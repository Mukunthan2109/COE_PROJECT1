import os
import sys
import shutil
from datetime import datetime, timedelta

# Add parent dir to path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from app import create_app
from app.models import db, User, Observation, ExpertReview, BatchProcurement, OutbreakAlert, DatasetMetadata
from ml.generate_dataset import main as generate_dataset
from ml.train import train_model

def setup_environment():
    print("==================================================")
    print("   SETTING UP 100% FULL PROJECT ENVIRONMENT      ")
    print("==================================================")

    # 1. Generate Expanded Dataset (9 crops, 18 categories)
    generate_dataset()

    # 2. Train Model
    train_model()

    # 3. Initialize Flask DB and seed default users & records
    app = create_app()
    with app.app_context():
        db.create_all()

        # Seed Users
        if User.query.count() == 0:
            print("Seeding default system users (Farmer, Expert, QA Manager)...")
            farmer_user = User(username="farmer1", email="farmer1@agri.org", role="farmer", region="North Zone")
            farmer_user.set_password("password123")

            expert_user = User(username="expert1", email="expert1@agri.org", role="expert", region="South Zone")
            expert_user.set_password("password123")

            qa_user = User(username="qamanager1", email="qa1@foodproc.com", role="qa_manager", region="Central Region")
            qa_user.set_password("password123")

            db.session.add_all([farmer_user, expert_user, qa_user])
            db.session.commit()
            print("Seeded default users!")

        # Seed Observations
        if Observation.query.count() == 0:
            print("Seeding initial demo observations...")
            now = datetime.utcnow()
            
            farmer_id = User.query.filter_by(role='farmer').first().id

            obs1 = Observation(
                user_id=farmer_id,
                crop="Tomato",
                symptom="Healthy",
                crop_stage="Vegetative",
                location_region="North Zone",
                image_path="uploads/demo_tomato_healthy.jpg",
                heatmap_path="heatmaps/heatmap_demo_tomato_healthy.jpg",
                observation_notes="Leaves looking healthy and green.",
                observation_timestamp=now - timedelta(hours=3),
                model_prediction="Tomato Healthy",
                confidence=0.92,
                explainability_notes="Uniform chlorophyll green color distribution; No prominent necrotic brown or black lesions detected.",
                status="Initial screening result"
            )

            obs2 = Observation(
                user_id=farmer_id,
                crop="Potato",
                symptom="Late Blight",
                crop_stage="Flowering",
                location_region="South Zone",
                image_path="uploads/demo_potato_blight.jpg",
                heatmap_path="heatmaps/heatmap_demo_potato_blight.jpg",
                observation_notes="Dark necrotic patches spreading on lower leaves after rain.",
                observation_timestamp=now - timedelta(hours=2, minutes=30),
                model_prediction="Potato Late Blight",
                confidence=0.64, # Low confidence -> triggers escalation
                explainability_notes="Significant leaf discoloration / yellowing index; Dark necrotic patches detected.",
                status="Needs expert review"
            )

            t_submit = now - timedelta(hours=5)
            obs3 = Observation(
                user_id=farmer_id,
                crop="Corn",
                symptom="Common Rust",
                crop_stage="Fruiting",
                location_region="South Zone",
                image_path="uploads/demo_corn_rust.jpg",
                heatmap_path="heatmaps/heatmap_demo_corn_rust.jpg",
                observation_notes="Brown pustules spreading on leaves.",
                observation_timestamp=t_submit,
                model_prediction="Corn Common Rust",
                confidence=0.58,
                explainability_notes="Visible dark spot clusters / necrotic lesion area; Rust pustules detected.",
                status="Reviewed by expert"
            )

            obs4 = Observation(
                user_id=farmer_id,
                crop="Potato",
                symptom="Late Blight",
                crop_stage="Flowering",
                location_region="South Zone",
                image_path="uploads/demo_potato_blight.jpg",
                heatmap_path="heatmaps/heatmap_demo_potato_blight.jpg",
                observation_notes="Another late blight incident in South Zone.",
                observation_timestamp=now - timedelta(hours=1),
                model_prediction="Potato Late Blight",
                confidence=0.61,
                explainability_notes="Dark necrotic patches detected.",
                status="Needs expert review"
            )

            obs5 = Observation(
                user_id=farmer_id,
                crop="Potato",
                symptom="Late Blight",
                crop_stage="Flowering",
                location_region="South Zone",
                image_path="uploads/demo_potato_blight.jpg",
                heatmap_path="heatmaps/heatmap_demo_potato_blight.jpg",
                observation_notes="Third late blight case in South Zone within 24h.",
                observation_timestamp=now - timedelta(minutes=30),
                model_prediction="Potato Late Blight",
                confidence=0.59,
                explainability_notes="Dark necrotic patches detected.",
                status="Needs expert review"
            )

            db.session.add_all([obs1, obs2, obs3, obs4, obs5])
            db.session.commit()

            # Add Expert Review
            expert_id = User.query.filter_by(role='expert').first().id
            t_review = t_submit + timedelta(minutes=14, seconds=20)
            time_to_review_sec = (t_review - t_submit).total_seconds()

            review3 = ExpertReview(
                observation_id=obs3.id,
                expert_user_id=expert_id,
                expert_label="Corn Common Rust (Confirmed)",
                expert_status="Confirmed",
                expert_comment="Confirmed Common Rust. Advise farmer to apply targeted fungicide spray.",
                review_timestamp=t_review,
                time_to_review_seconds=time_to_review_sec
            )
            db.session.add(review3)
            db.session.commit()

            # Seed static demo images into static/uploads and static/heatmaps
            uploads_dir = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
            heatmaps_dir = os.path.join(BASE_DIR, 'app', 'static', 'heatmaps')
            os.makedirs(uploads_dir, exist_ok=True)
            os.makedirs(heatmaps_dir, exist_ok=True)

            dataset_img_dir = os.path.join(BASE_DIR, 'dataset', 'images')
            for src_name, dst_name in [
                ("tomato_healthy_01.jpg", "demo_tomato_healthy.jpg"),
                ("potato_late_blight_01.jpg", "demo_potato_blight.jpg"),
                ("corn_common_rust_01.jpg", "demo_corn_rust.jpg")
            ]:
                src_p = os.path.join(dataset_img_dir, src_name)
                dst_p = os.path.join(uploads_dir, dst_name)
                if os.path.exists(src_p):
                    shutil.copy(src_p, dst_p)

            # Generate Grad-CAM heatmaps for demo images
            from ml.gradcam import generate_gradcam_heatmap
            for img_name in ["demo_tomato_healthy.jpg", "demo_potato_blight.jpg", "demo_corn_rust.jpg"]:
                p = os.path.join(uploads_dir, img_name)
                if os.path.exists(p):
                    generate_gradcam_heatmap(p, f"heatmap_{img_name}")

            print("Seeded demo database with initial observations and expert review!")

        # Seed Batch Procurements
        if BatchProcurement.query.count() == 0:
            print("Seeding demo food-processing crop batch procurements...")
            b1 = BatchProcurement(
                batch_code="BATCH-TOM-88A19B",
                crop="Tomato",
                supplier_region="North Zone",
                total_weight_kg=3500.0,
                sample_size_count=100,
                diseased_sample_count=2,
                defect_rate_percent=2.0,
                quality_grade="Grade A",
                intake_status="Approved",
                inspection_notes="Clean delivery batch. Approved for premium sauce processing."
            )
            b2 = BatchProcurement(
                batch_code="BATCH-POT-C4F22A",
                crop="Potato",
                supplier_region="South Zone",
                total_weight_kg=5000.0,
                sample_size_count=100,
                diseased_sample_count=12,
                defect_rate_percent=12.0,
                quality_grade="Grade B",
                intake_status="Conditional (Sorting)",
                inspection_notes="Moderate late blight lesions. Requires mechanical sorting prior to peeling."
            )
            b3 = BatchProcurement(
                batch_code="BATCH-CRN-F910B8",
                crop="Corn",
                supplier_region="East District",
                total_weight_kg=4200.0,
                sample_size_count=100,
                diseased_sample_count=28,
                defect_rate_percent=28.0,
                quality_grade="REJECT",
                intake_status="Rejected Intake",
                inspection_notes="Severe rust contamination exceeding 25% defect threshold. Rejected intake."
            )
            db.session.add_all([b1, b2, b3])
            db.session.commit()
            print("Seeded demo crop batch procurements!")

        # Seed Outbreak Alert
        if OutbreakAlert.query.count() == 0:
            print("Triggering initial outbreak alert check...")
            from app.services.analytics_service import check_and_trigger_outbreak_alerts
            check_and_trigger_outbreak_alerts(threshold=3)

    print("\n100% Full Environment Setup Complete!")

if __name__ == '__main__':
    setup_environment()
