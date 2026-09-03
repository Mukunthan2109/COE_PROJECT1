import os
import sys
from datetime import datetime, timedelta

# Add parent dir to path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from app import create_app
from app.models import db, Observation, ExpertReview, DatasetMetadata
from ml.generate_dataset import main as generate_dataset
from ml.train import train_model

def setup_environment():
    print("==================================================")
    print("   SETTING UP FARMER APP ENVIRONMENT & DATASET   ")
    print("==================================================")

    # 1. Generate Demo Dataset
    generate_dataset()

    # 2. Train ML Baseline Model
    train_model()

    # 3. Initialize Flask DB and seed demo observations
    app = create_app()
    with app.app_context():
        db.create_all()

        # Check if seed observations already exist
        if Observation.query.count() == 0:
            print("Seeding initial demo observations for Review 1 evaluation...")

            now = datetime.utcnow()
            
            # Case 1: High Confidence Screening Result (Tomato Healthy)
            obs1 = Observation(
                crop="Tomato",
                symptom="Healthy",
                crop_stage="Vegetative",
                location_region="North Zone",
                image_path="uploads/demo_tomato_healthy.jpg",
                observation_notes="Leaves looking healthy and green.",
                observation_timestamp=now - timedelta(hours=3),
                model_prediction="Tomato Healthy",
                confidence=0.88,
                explainability_notes="Uniform chlorophyll green color distribution; No prominent necrotic brown or black lesions detected.",
                status="Initial screening result"
            )

            # Case 2: Low Confidence Escalated Observation (Tomato Leaf Spot)
            obs2 = Observation(
                crop="Tomato",
                symptom="Leaf Spot",
                crop_stage="Fruiting",
                location_region="South Zone",
                image_path="uploads/demo_tomato_spot.jpg",
                observation_notes="Small dark spots appeared on lower leaves after rain.",
                observation_timestamp=now - timedelta(hours=2, minutes=30),
                model_prediction="Tomato Leaf Spot",
                confidence=0.62, # Low confidence -> triggers escalation
                explainability_notes="Visible dark spot clusters detected (approx 4.2% surface area); Irregular leaf surface texture detected.",
                status="Needs expert review"
            )

            # Case 3: Pre-Reviewed Escalated Observation (Potato Late Blight)
            t_submit = now - timedelta(hours=5)
            obs3 = Observation(
                crop="Potato",
                symptom="Early Blight",
                crop_stage="Flowering",
                location_region="East District",
                image_path="uploads/demo_potato_blight.jpg",
                observation_notes="Brown patches spreading on outer leaves.",
                observation_timestamp=t_submit,
                model_prediction="Potato Late Blight",
                confidence=0.55,
                explainability_notes="Significant leaf discoloration / yellowing index; Dark necrotic patches detected.",
                status="Reviewed by expert"
            )

            db.session.add_all([obs1, obs2, obs3])
            db.session.commit()

            # Add Expert Review for Case 3
            t_review = t_submit + timedelta(minutes=14, seconds=20) # 14m 20s review time
            time_to_review_sec = (t_review - t_submit).total_seconds()

            review3 = ExpertReview(
                observation_id=obs3.id,
                expert_label="Potato Late Blight (Confirmed)",
                expert_status="Confirmed",
                expert_comment="Confirmed Late Blight. Advise farmer to apply targeted fungicide and segregate batch from food processing intake.",
                review_timestamp=t_review,
                time_to_review_seconds=time_to_review_sec
            )
            db.session.add(review3)
            db.session.commit()

            # Seed static demo images into static/uploads
            uploads_dir = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            # Copy sample images from dataset/images to uploads for demo viewing
            dataset_img_dir = os.path.join(BASE_DIR, 'dataset', 'images')
            import shutil
            for src_name, dst_name in [
                ("tomato_healthy_01.jpg", "demo_tomato_healthy.jpg"),
                ("tomato_leaf_spot_01.jpg", "demo_tomato_spot.jpg"),
                ("potato_late_blight_01.jpg", "demo_potato_blight.jpg")
            ]:
                src_p = os.path.join(dataset_img_dir, src_name)
                dst_p = os.path.join(uploads_dir, dst_name)
                if os.path.exists(src_p):
                    shutil.copy(src_p, dst_p)

            print("Seeded demo database with initial observations and expert review!")

    print("\nEnvironment setup complete!")

if __name__ == '__main__':
    setup_environment()
