import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, current_app as app
from werkzeug.utils import secure_filename

from app.models import db, Observation, ExpertReview, DatasetMetadata
from app.services.image_quality import evaluate_image_quality
from app.services.predictor import predict_crop_disease
from app.services.escalation import determine_escalation, calculate_time_to_review, get_escalation_analytics, get_baseline_vs_mvp_comparison

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/')
def index():
    recent_observations = Observation.query.order_by(Observation.created_at.desc()).limit(5).all()
    analytics = get_escalation_analytics()
    return render_template('index.html', recent=recent_observations, analytics=analytics)

@main_bp.route('/observe', methods=['GET', 'POST'])
def observe():
    if request.method == 'GET':
        return render_template('observe.html')

    crop = request.form.get('crop', '').strip()
    symptom = request.form.get('symptom', '').strip()
    crop_stage = request.form.get('crop_stage', '').strip()
    location_region = request.form.get('location_region', '').strip()
    notes = request.form.get('observation_notes', '').strip()

    # Form Validation
    if not crop or not symptom or not crop_stage or not location_region:
        flash('Please fill in all required observation fields.', 'danger')
        return render_template('observe.html', form_data=request.form)

    if 'crop_image' not in request.files:
        flash('Please select a crop image file to upload.', 'danger')
        return render_template('observe.html', form_data=request.form)

    file = request.files['crop_image']
    if file.filename == '':
        flash('No file selected for upload.', 'danger')
        return render_template('observe.html', form_data=request.form)

    if not allowed_file(file.filename):
        flash('Invalid image format. Allowed formats: PNG, JPG, JPEG, WEBP.', 'danger')
        return render_template('observe.html', form_data=request.form)

    # Save uploaded image safely
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex[:12]}_{secure_filename(file.filename)}"
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(save_path)
    
    relative_image_path = f"uploads/{unique_filename}"

    # Step 1: Image Quality Verification
    is_quality_valid, quality_msg, quality_details = evaluate_image_quality(save_path)
    
    if not is_quality_valid:
        flash(quality_msg, 'danger')
        return render_template('observe.html', 
                               form_data=request.form, 
                               quality_failed=True, 
                               quality_details=quality_details)

    # Step 2: ML Triage & Prediction
    pred_res = predict_crop_disease(save_path, crop, symptom)
    prediction = pred_res['prediction']
    confidence = pred_res['confidence']
    explainability = "; ".join(pred_res['explainability'])
    is_supported = pred_res['is_supported']

    # Step 3: Confidence & Escalation Logic
    status = determine_escalation(
        confidence, 
        is_supported=is_supported, 
        threshold=current_app.config['CONFIDENCE_THRESHOLD']
    )

    # Step 4: Database Storage
    observation = Observation(
        crop=crop,
        symptom=symptom,
        crop_stage=crop_stage,
        location_region=location_region,
        image_path=relative_image_path,
        observation_notes=notes,
        observation_timestamp=datetime.utcnow(),
        model_prediction=prediction,
        confidence=confidence,
        explainability_notes=explainability,
        status=status
    )
    db.session.add(observation)
    db.session.commit()

    return redirect(url_for('main.result', id=observation.id))


@main_bp.route('/result/<int:id>')
def result(id):
    observation = Observation.query.get_or_404(id)
    explainability_list = [item.strip() for item in (observation.explainability_notes or "").split(";") if item.strip()]
    threshold = current_app.config['CONFIDENCE_THRESHOLD']
    return render_template('result.html', observation=observation, explainability=explainability_list, threshold=threshold)


@main_bp.route('/status', methods=['GET'])
def status():
    query_id = request.args.get('id', type=int)
    search_result = None
    if query_id:
        search_result = Observation.query.get(query_id)
        if not search_result:
            flash(f"Observation ID #{query_id} not found.", "warning")

    all_observations = Observation.query.order_by(Observation.created_at.desc()).all()
    return render_template('status.html', observations=all_observations, search_result=search_result, query_id=query_id)


@main_bp.route('/expert')
def expert_dashboard():
    pending_escalations = Observation.query.filter_by(status='Needs expert review').order_by(Observation.created_at.asc()).all()
    reviewed_observations = Observation.query.filter_by(status='Reviewed by expert').order_by(Observation.created_at.desc()).all()
    all_observations = Observation.query.order_by(Observation.created_at.desc()).all()
    
    analytics = get_escalation_analytics()
    comparison = get_baseline_vs_mvp_comparison()

    return render_template('expert.html', 
                           pending=pending_escalations, 
                           reviewed=reviewed_observations, 
                           all_obs=all_observations, 
                           analytics=analytics,
                           comparison=comparison)


@main_bp.route('/expert/review/<int:id>', methods=['GET', 'POST'])
def expert_review(id):
    observation = Observation.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('expert_review.html', observation=observation)

    expert_label = request.form.get('expert_label', '').strip()
    expert_status = request.form.get('expert_status', 'Confirmed').strip()
    expert_comment = request.form.get('expert_comment', '').strip()

    if not expert_label:
        flash("Please specify the confirmed/corrected expert diagnosis label.", "danger")
        return render_template('expert_review.html', observation=observation)

    review_time = datetime.utcnow()
    time_to_review_sec = calculate_time_to_review(observation.observation_timestamp, review_time)

    # Check if review already exists
    existing_review = ExpertReview.query.filter_by(observation_id=observation.id).first()
    if existing_review:
        existing_review.expert_label = expert_label
        existing_review.expert_status = expert_status
        existing_review.expert_comment = expert_comment
        existing_review.review_timestamp = review_time
        existing_review.time_to_review_seconds = time_to_review_sec
    else:
        review = ExpertReview(
            observation_id=observation.id,
            expert_label=expert_label,
            expert_status=expert_status,
            expert_comment=expert_comment,
            review_timestamp=review_time,
            time_to_review_seconds=time_to_review_sec
        )
        db.session.add(review)

    observation.status = 'Reviewed by expert'
    db.session.commit()

    flash(f"Expert review submitted for Observation #{observation.id}! Time to review: {ExpertReview.query.filter_by(observation_id=observation.id).first().format_time_to_review()}", "success")
    return redirect(url_for('main.expert_dashboard'))
