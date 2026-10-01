import os
import sys
from datetime import datetime, timedelta

# Ensure parent directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, User, Observation, ExpertReview

def seed_demo_data():
    app = create_app()
    with app.app_context():
        print("Seeding AgriShield DEMO DATA...")
        
        # 1. Create Demo Users (if not existing)
        expert = User.query.filter_by(username='demo_expert').first()
        if not expert:
            expert = User(username='demo_expert', email='expert@agrishield.org', role='expert', region='North Zone')
            expert.set_password('expert123')
            db.session.add(expert)

        farmer = User.query.filter_by(username='demo_farmer').first()
        if not farmer:
            farmer = User(username='demo_farmer', email='farmer@agrishield.org', role='farmer', region='North Zone')
            farmer.set_password('farmer123')
            db.session.add(farmer)

        db.session.commit()

        now = datetime.utcnow()

        demo_cases = [
            {
                'crop': 'Tomato',
                'symptom': 'Healthy',
                'crop_stage': 'Seedling',
                'location_region': 'North Zone',
                'image_path': 'dataset/images/tomato_healthy_01.jpg',
                'model_prediction': 'Tomato Healthy',
                'confidence': 0.94,
                'risk_level': 'Low',
                'status': 'Initial screening result',
                'notes': '[DEMO DATA] Normal high-confidence healthy screening case.',
                'symptom_hours_ago': 2,
                'reviewed': False
            },
            {
                'crop': 'Potato',
                'symptom': 'Brown spots',
                'crop_stage': 'Vegetative',
                'location_region': 'South Zone',
                'image_path': 'dataset/images/potato_early_blight_01.jpg',
                'model_prediction': 'Potato Early Blight',
                'confidence': 0.88,
                'risk_level': 'High',
                'status': 'Initial screening result',
                'notes': '[DEMO DATA] High-confidence early blight case.',
                'symptom_hours_ago': 5,
                'reviewed': False
            },
            {
                'crop': 'Rice',
                'symptom': 'Brown spots',
                'crop_stage': 'Flowering',
                'location_region': 'Central Region',
                'image_path': 'dataset/images/rice_brown_spot_01.jpg',
                'model_prediction': 'Rice Brown Spot',
                'confidence': 0.62,
                'risk_level': 'High',
                'status': 'Needs expert review',
                'notes': '[DEMO DATA] Low-confidence screening case escalated to expert queue.',
                'symptom_hours_ago': 12,
                'reviewed': False
            },
            {
                'crop': 'Maize',
                'symptom': 'Yellowing leaves',
                'crop_stage': 'Fruiting',
                'location_region': 'East District',
                'image_path': 'dataset/images/maize_common_rust_01.jpg',
                'model_prediction': 'Maize Common Rust',
                'confidence': 0.65,
                'risk_level': 'High',
                'status': 'Reviewed by expert',
                'notes': '[DEMO DATA] Completed expert review case.',
                'symptom_hours_ago': 24,
                'reviewed': True,
                'expert_label': 'Maize Common Rust (Confirmed)',
                'expert_status': 'Validated (Confirmed)',
                'expert_comment': 'Confirmed common rust symptoms on lower maize leaves. Recommended copper fungicide spray.',
                'review_minutes': 45
            },
            {
                'crop': 'Chili',
                'symptom': 'Leaf curling',
                'crop_stage': 'Vegetative',
                'location_region': 'West Valley',
                'image_path': 'dataset/images/chili_leaf_curl_01.jpg',
                'model_prediction': 'Chili Leaf Curl',
                'confidence': 0.81,
                'risk_level': 'Medium',
                'status': 'Initial screening result',
                'notes': '[DEMO DATA] Expanded crop chili leaf curl screening.',
                'symptom_hours_ago': 3,
                'reviewed': False
            }
        ]

        seeded_count = 0
        for case in demo_cases:
            first_sym_time = now - timedelta(hours=case['symptom_hours_ago'])
            obs = Observation(
                user_id=farmer.id,
                crop=case['crop'],
                symptom=case['symptom'],
                crop_stage=case['crop_stage'],
                location_region=case['location_region'],
                image_path=case['image_path'],
                observation_notes=case['notes'],
                observation_timestamp=first_sym_time + timedelta(minutes=10),
                first_symptom_time=first_sym_time,
                model_prediction=case['model_prediction'],
                confidence=case['confidence'],
                risk_level=case['risk_level'],
                explainability_notes=f"Visual indicators: Dark spot ratio 0.12, GLCM contrast 0.45. [DEMO DATA]",
                status=case['status']
            )
            db.session.add(obs)
            db.session.flush()

            if case.get('reviewed'):
                rev_comp = obs.observation_timestamp + timedelta(minutes=case['review_minutes'])
                rev = ExpertReview(
                    observation_id=obs.id,
                    expert_user_id=expert.id,
                    expert_label=case['expert_label'],
                    expert_status=case['expert_status'],
                    expert_comment=case['expert_comment'],
                    review_timestamp=rev_comp,
                    time_to_review_seconds=float((rev_comp - first_sym_time).total_seconds())
                )
                db.session.add(rev)

            seeded_count += 1

        db.session.commit()
        print(f"Successfully seeded {seeded_count} DEMO DATA observations into SQLite database!")

if __name__ == '__main__':
    seed_demo_data()
