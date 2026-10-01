import os
import uuid
from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from app.models import db, User, Observation, ExpertReview, BatchProcurement, OutbreakAlert, DatasetMetadata
from app.services.image_quality import evaluate_image_quality, compute_image_hash
from app.services.predictor import predict_crop_disease
from app.services.escalation import determine_escalation, calculate_time_to_review, get_escalation_analytics, get_baseline_vs_mvp_comparison
from app.services.batch_qa_service import create_batch_inspection
from app.services.analytics_service import get_dashboard_analytics_payload
from app.translations import get_translation, TRANSLATIONS

main_bp = Blueprint('main', __name__)

@main_bp.context_processor
def inject_translations():
    lang = session.get('lang', request.args.get('lang', 'en'))
    if lang not in ['en', 'ta']:
        lang = 'en'
    def t(key):
        return get_translation(lang, key)
    return dict(t=t, current_lang=lang, TRANSLATIONS=TRANSLATIONS)

@main_bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'ta']:
        session['lang'] = lang
    next_page = request.referrer or url_for('main.index')
    return redirect(next_page)


@main_bp.route('/health')
def health():
    return jsonify({'status': 'ok'})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access this feature.", "warning")
                return redirect(url_for('main.login', next=request.url))
            if current_user.role not in roles:
                flash("Access denied. Authorized role permission required.", "danger")
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- AUTHENTICATION ROUTES ---

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        flash(f"Welcome back, {user.username}! Logged in as {user.role.title()}.", "success")
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))

    flash("Invalid username or password.", "danger")
    return render_template('login.html')


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    role = request.form.get('role', 'farmer').strip()
    region = request.form.get('region', 'North Zone').strip()

    if not username or not email or not password:
        flash("Please fill in all required registration fields.", "danger")
        return render_template('register.html')

    if User.query.filter_by(username=username).first():
        flash("Username already taken. Please choose another.", "danger")
        return render_template('register.html')

    user = User(username=username, email=email, role=role, region=region)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    flash("Account registered successfully!", "success")
    return redirect(url_for('main.index'))


@main_bp.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('main.index'))


# --- CORE AGRISHIELD WORKFLOW ROUTES ---

@main_bp.route('/')
def index():
    from app.services.predictor import MODEL_DIR
    model_path = os.path.join(MODEL_DIR, 'model.pkl')
    encoder_path = os.path.join(MODEL_DIR, 'label_encoder.pkl')
    model_operational = os.path.exists(model_path) and os.path.exists(encoder_path)

    payload = get_dashboard_analytics_payload()

    total_obs = payload['total_observations']
    high_risk_count = payload['high_risk_count']
    pending_count = payload['pending_count']
    crop_counts = payload['crop_counts']

    if total_obs == 0:
        dynamic_insight_en = "Not enough observations to generate a crop health trend."
        dynamic_insight_ta = "பயிர் ஆரோக்கியப் போக்கை உருவாக்க போதுமான கவனிப்புகள் இல்லை."
    elif high_risk_count > 0:
        dynamic_insight_en = f"{high_risk_count} high-risk case(s) flagged for immediate expert triage."
        dynamic_insight_ta = f"{high_risk_count} அவசர ஆபத்து வழக்குகள் உடனடி நிபுணர் கவனிப்பிற்கு அனுப்பப்பட்டுள்ளன."
    elif pending_count > 0:
        dynamic_insight_en = "Most recent cases are currently awaiting expert review."
        dynamic_insight_ta = "சமீபத்திய வழக்குகள் தற்போது நிபுணர் பரிசீலனைக்கு காத்திருக்கின்றன."
    else:
        top_crop = max(crop_counts.items(), key=lambda x: x[1])[0] if crop_counts else "Tomato"
        dynamic_insight_en = f"{top_crop} observations are currently the most frequently submitted crop."
        dynamic_insight_ta = f"தற்போது {top_crop} பயிர் கவனிப்புகள் அதிகம் சமர்ப்பிக்கப்பட்டுள்ளன."

    pending_queue = Observation.query.filter_by(status='Needs expert review').order_by(Observation.created_at.desc()).limit(5).all()
    recent_observations = Observation.query.order_by(Observation.created_at.desc()).limit(8).all()
    active_alerts = OutbreakAlert.query.filter_by(status='Active').all()

    dashboard_data = {
        'model_operational': model_operational,
        'total_observations': total_obs,
        'ai_screened_count': payload['ai_screened_count'],
        'pending_count': pending_count,
        'reviewed_count': payload['reviewed_count'],
        'escalated_count': payload['escalated_count'],
        'high_risk_count': high_risk_count,
        'avg_review_time': payload['avg_review_time'],
        'escalation_rate_pct': payload['escalation_rate_pct'],
        'disease_counts': payload['disease_counts'],
        'crop_counts': crop_counts,
        'avg_confidence': payload['avg_confidence'],
        'high_conf_count': payload['high_conf_count'],
        'med_conf_count': payload['med_conf_count'],
        'low_conf_count': payload['low_conf_count'],
        'pending_queue': pending_queue,
        'recent_observations': recent_observations,
        'dynamic_insight_en': dynamic_insight_en,
        'dynamic_insight_ta': dynamic_insight_ta,
        'active_alerts': active_alerts
    }

    return render_template('index.html', d=dashboard_data, analytics=payload['summary'], alerts=active_alerts, recent=recent_observations)




@main_bp.route('/observe', methods=['GET', 'POST'])
def observe():
    if request.method == 'GET':
        return render_template('observe.html')

    crop = request.form.get('crop', 'Tomato').strip()
    if crop in ("Corn", "Maize"):
        crop = "Maize"
    symptom = request.form.get('symptom', 'Yellowing leaves').strip()
    crop_stage = request.form.get('crop_stage', 'Vegetative').strip()
    location_region = request.form.get('location_region', 'Coimbatore').strip()
    notes = request.form.get('observation_notes', '').strip()
    first_symptom_str = request.form.get('first_symptom_time', '').strip()

    first_symptom_time = datetime.utcnow()
    if first_symptom_str:
        try:
            first_symptom_time = datetime.strptime(first_symptom_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            try:
                first_symptom_time = datetime.strptime(first_symptom_str, '%Y-%m-%d %H:%M')
            except ValueError:
                pass

    if not crop_stage or not location_region:
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

    unique_filename = f"{uuid.uuid4().hex[:12]}_{secure_filename(file.filename)}"
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(save_path)
    
    relative_image_path = f"uploads/{unique_filename}"

    # Step 1: Image Quality Inspection
    is_quality_valid, quality_msg, quality_details = evaluate_image_quality(save_path)
    if not is_quality_valid:
        flash(quality_msg, 'danger')
        return render_template('observe.html', 
                               form_data=request.form, 
                               quality_failed=True, 
                               quality_details=quality_details)

    # Step 1b: Duplicate Image Hash Check
    img_hash = compute_image_hash(save_path)
    existing_obs = Observation.query.filter_by(image_hash=img_hash).first()
    if existing_obs:
        flash(f"⚠️ Duplicate Image Detected: An observation with the exact same image photo was previously submitted (Observation #{existing_obs.id}). Redirecting to existing record.", "warning")
        return redirect(url_for('main.observation_detail', id=existing_obs.id))

    # Step 2: ML / DL Disease Triage & Grad-CAM visual heatmap
    pred_res = predict_crop_disease(save_path, crop, symptom)
    prediction = pred_res['prediction']
    confidence = pred_res['confidence']
    risk_level = pred_res.get('risk_level', 'Medium')
    explainability = "; ".join(pred_res['explainability'])
    is_supported = pred_res['is_supported']
    heatmap_path = pred_res.get('heatmap_path')

    if crop in ('Auto', 'Detect', '', None):
        crop = pred_res.get('detected_crop', 'Tomato')
    if symptom in ('Auto', 'Detect', '', None):
        symptom = pred_res.get('detected_symptom', 'Healthy')

    # Step 3: Confidence & Escalation Logic
    status = determine_escalation(
        confidence, 
        is_supported=is_supported, 
        threshold=current_app.config['CONFIDENCE_THRESHOLD']
    )

    # Step 4: Database Storage
    user_id = current_user.id if current_user.is_authenticated else None
    observation = Observation(
        user_id=user_id,
        crop=crop,
        symptom=symptom,
        crop_stage=crop_stage,
        location_region=location_region,
        image_path=relative_image_path,
        heatmap_path=heatmap_path,
        observation_notes=notes,
        observation_timestamp=datetime.utcnow(),
        first_symptom_time=first_symptom_time,
        image_hash=img_hash,
        model_prediction=prediction,
        confidence=confidence,
        risk_level=risk_level,
        explainability_notes=explainability,
        status=status
    )
    db.session.add(observation)
    db.session.commit()

    return redirect(url_for('main.observation_detail', id=observation.id))


@main_bp.route('/scan', methods=['GET', 'POST'])
def scan():
    """
    Instant AI Disease Scanner: User uploads photo manually, ML model auto-analyzes disease and crop.
    """
    if request.method == 'GET':
        return render_template('scan.html')

    if 'crop_image' not in request.files:
        flash('Please select a plant photo file to analyze.', 'danger')
        return render_template('scan.html')

    file = request.files['crop_image']
    if file.filename == '' or not allowed_file(file.filename):
        flash('Invalid image file format. Allowed: PNG, JPG, JPEG, WEBP.', 'danger')
        return render_template('scan.html')

    unique_filename = f"scan_{uuid.uuid4().hex[:12]}_{secure_filename(file.filename)}"
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(save_path)
    relative_image_path = f"uploads/{unique_filename}"

    # Step 1: Image Quality Inspection
    is_quality_valid, quality_msg, quality_details = evaluate_image_quality(save_path)
    if not is_quality_valid:
        flash(quality_msg, 'danger')
        return render_template('scan.html', quality_failed=True, quality_details=quality_details)

    # Step 1b: Duplicate Check
    img_hash = compute_image_hash(save_path)
    existing_obs = Observation.query.filter_by(image_hash=img_hash).first()
    if existing_obs:
        flash(f"⚠️ Duplicate Image Detected: Exact same photo previously recorded (#Observation {existing_obs.id}).", "warning")
        return redirect(url_for('main.observation_detail', id=existing_obs.id))

    # Step 2: Disease Analysis within Selected Crop
    crop = request.form.get('crop', 'Tomato').strip()
    if crop in ("Corn", "Maize"):
        crop = "Maize"
    pred_res = predict_crop_disease(save_path, crop=crop, symptom="Auto")
    prediction = pred_res['prediction']
    confidence = pred_res['confidence']
    risk_level = pred_res.get('risk_level', 'Medium')
    detected_crop = pred_res.get('detected_crop', 'Tomato')
    detected_symptom = pred_res.get('detected_symptom', 'Healthy')
    explainability = pred_res['explainability']
    heatmap_path = pred_res.get('heatmap_path')

    status = determine_escalation(
        confidence, 
        is_supported=pred_res['is_supported'], 
        threshold=current_app.config['CONFIDENCE_THRESHOLD']
    )

    user_id = current_user.id if current_user.is_authenticated else None
    observation = Observation(
        user_id=user_id,
        crop=detected_crop,
        symptom=detected_symptom,
        crop_stage="Vegetative",
        location_region="Coimbatore",
        image_path=relative_image_path,
        heatmap_path=heatmap_path,
        observation_notes="Instant AI Scan Observation",
        observation_timestamp=datetime.utcnow(),
        first_symptom_time=datetime.utcnow(),
        image_hash=img_hash,
        model_prediction=prediction,
        confidence=confidence,
        risk_level=risk_level,
        explainability_notes="; ".join(explainability),
        status=status
    )
    db.session.add(observation)
    db.session.commit()

    return render_template('scan.html',
                           result=pred_res,
                           observation=observation,
                           image_path=relative_image_path,
                           heatmap_path=heatmap_path,
                           status=status,
                           confidence_pct=f"{round(confidence * 100, 1)}%",
                           quality_msg=quality_msg)


@main_bp.route('/api/analyze-image', methods=['POST'])
def analyze_image_api():
    """
    AJAX Endpoint: Instant client-side analysis when selecting an image.
    """
    if 'crop_image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file uploaded'}), 400
        
    file = request.files['crop_image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid image file format'}), 400

    unique_filename = f"api_{uuid.uuid4().hex[:12]}_{secure_filename(file.filename)}"
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(save_path)

    is_quality_valid, quality_msg, quality_details = evaluate_image_quality(save_path)
    if not is_quality_valid:
        return jsonify({
            'success': False,
            'quality_failed': True,
            'error': quality_msg,
            'quality_details': quality_details
        }), 400

    crop = request.form.get('crop', 'Auto').strip()
    symptom = request.form.get('symptom', 'Auto').strip()

    pred_res = predict_crop_disease(save_path, crop, symptom)
    detected_crop = pred_res.get('detected_crop', 'Tomato')
    detected_symptom = pred_res.get('detected_symptom', 'Healthy')
    prediction = pred_res['prediction']
    confidence = pred_res['confidence']
    heatmap_path = pred_res.get('heatmap_path')

    status = determine_escalation(
        confidence, 
        is_supported=pred_res['is_supported'], 
        threshold=current_app.config['CONFIDENCE_THRESHOLD']
    )

    qa_impact = "Grade A (Prime Quality)"
    if "Blight" in prediction or "Rot" in prediction:
        qa_impact = "REJECT (Unusable Batch / Severe Infection)"
    elif "Spot" in prediction or "Rust" in prediction or "Curl" in prediction:
        qa_impact = "Grade C (Substandard Quality / Discounted)"
    elif "Discoloration" in prediction or "Yellowing" in prediction:
        qa_impact = "Grade B (Minor Quality Concern)"

    return jsonify({
        'success': True,
        'image_url': f"/static/uploads/{unique_filename}",
        'heatmap_url': f"/static/{heatmap_path}" if heatmap_path else None,
        'detected_crop': detected_crop,
        'detected_symptom': detected_symptom,
        'prediction': prediction,
        'confidence': confidence,
        'confidence_pct': f"{round(confidence * 100, 1)}%",
        'status': status,
        'explainability': pred_res['explainability'],
        'qa_impact': qa_impact,
        'quality_msg': quality_msg
    })


@main_bp.route('/observation/<int:id>')
@main_bp.route('/result/<int:id>')
def observation_detail(id):
    observation = db.session.get(Observation, id)
    if not observation:
        flash("Observation record not found.", "danger")
        return redirect(url_for('main.index'))

    explainability_list = [item.strip() for item in (observation.explainability_notes or "").split(";") if item.strip()]
    threshold = current_app.config['CONFIDENCE_THRESHOLD']
    return render_template('observation_detail.html', observation=observation, explainability=explainability_list, threshold=threshold)


@main_bp.route('/result_legacy/<int:id>')
def result(id):
    return redirect(url_for('main.observation_detail', id=id))


@main_bp.route('/history', methods=['GET'], endpoint='history')
@main_bp.route('/status', methods=['GET'], endpoint='status')
def history():
    selected_crop = request.args.get('crop', '').strip()
    selected_status = request.args.get('status', '').strip()
    query_id = request.args.get('id', type=int)

    query = Observation.query

    if query_id:
        query = query.filter_by(id=query_id)
    if selected_crop:
        query = query.filter_by(crop=selected_crop)
    if selected_status:
        query = query.filter_by(status=selected_status)

    all_observations = query.order_by(Observation.created_at.desc()).all()
    return render_template('history.html', 
                           observations=all_observations, 
                           selected_crop=selected_crop, 
                           selected_status=selected_status)


# --- EXPERT PORTAL ---

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
    observation = db.session.get(Observation, id)
    if not observation:
        flash("Observation not found.", "danger")
        return redirect(url_for('main.expert_dashboard'))

    if request.method == 'GET':
        return render_template('expert_review.html', observation=observation)

    expert_label = request.form.get('expert_label', '').strip()
    expert_status = request.form.get('expert_status', '').strip()
    expert_comment = request.form.get('expert_comment', '').strip()

    valid_statuses = {'Validated (Confirmed)', 'Not Confirmed', 'Needs More Information'}
    if not expert_status or expert_status not in valid_statuses:
        flash("Please select a valid expert review status from the dropdown options.", "danger")
        return render_template('expert_review.html', observation=observation)

    if not expert_label:
        flash("Please specify the confirmed/corrected expert diagnosis label.", "danger")
        return render_template('expert_review.html', observation=observation)

    review_time = datetime.utcnow()
    start_time = observation.first_symptom_time if observation.first_symptom_time else observation.observation_timestamp
    time_to_review_sec = calculate_time_to_review(start_time, review_time)
    expert_user_id = current_user.id if current_user.is_authenticated else None

    existing_review = ExpertReview.query.filter_by(observation_id=observation.id).first()
    if existing_review:
        existing_review.expert_user_id = expert_user_id
        existing_review.expert_label = expert_label
        existing_review.expert_status = expert_status
        existing_review.expert_comment = expert_comment
        existing_review.review_timestamp = review_time
        existing_review.time_to_review_seconds = time_to_review_sec
    else:
        review = ExpertReview(
            observation_id=observation.id,
            expert_user_id=expert_user_id,
            expert_label=expert_label,
            expert_status=expert_status,
            expert_comment=expert_comment,
            review_timestamp=review_time,
            time_to_review_seconds=time_to_review_sec
        )
        db.session.add(review)

    observation.status = 'Reviewed by expert'
    db.session.commit()

    flash(f"Expert review submitted for Observation #{observation.id}! Recorded SLA Time to Review.", "success")
    return redirect(url_for('main.expert_dashboard'))


# --- ANALYTICS, EVALUATION & FEEDBACK ROUTES ---

@main_bp.route('/analytics')
def analytics_dashboard():
    payload = get_dashboard_analytics_payload()
    return render_template('analytics.html', payload=payload)


@main_bp.route('/evaluation')
def evaluation():
    import json
    metrics_path = os.path.abspath(os.path.join(current_app.root_path, '..', 'ml', 'saved_model', 'metrics.json'))
    metrics = None
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, 'r', encoding='utf-8') as f:
                metrics = json.load(f)
        except Exception:
            metrics = None
    return render_template('evaluation.html', metrics=metrics)


@main_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'GET':
        return render_template('feedback.html')

    role = request.form.get('user_role', 'Farmer')
    rating = request.form.get('rating', '5')
    comments = request.form.get('comments', '')

    flash("Thank you for your feedback! Your evaluation has been recorded.", "success")
    return redirect(url_for('main.index'))


@main_bp.route('/batch_qa', methods=['GET', 'POST'])
def batch_qa():
    if request.method == 'GET':
        recent_batches = BatchProcurement.query.order_by(BatchProcurement.created_at.desc()).all()
        return render_template('batch_qa.html', batches=recent_batches)

    crop = request.form.get('crop', '').strip()
    supplier_region = request.form.get('supplier_region', '').strip()
    total_weight_kg = request.form.get('total_weight_kg', type=float)
    sample_size = request.form.get('sample_size_count', type=int)
    diseased_count = request.form.get('diseased_sample_count', type=int)
    notes = request.form.get('inspection_notes', '').strip()

    batch = create_batch_inspection(crop, supplier_region, total_weight_kg, sample_size, diseased_count, notes)
    flash(f"Batch #{batch.batch_code} recorded successfully! Quality Status: {batch.procurement_status}.", "success")
    return redirect(url_for('main.batch_qa'))


@main_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@main_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
