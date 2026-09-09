import pytest
from datetime import datetime, timedelta
from app import create_app
from app.models import db, Observation, OutbreakAlert
from app.services.analytics_service import check_and_trigger_outbreak_alerts

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

def test_outbreak_alert_trigger(client):
    with client.application.app_context():
        now = datetime.utcnow()
        # Create 3 observations of Potato Late Blight in South Zone within 48h
        for i in range(3):
            obs = Observation(
                crop="Potato",
                symptom="Late Blight",
                crop_stage="Flowering",
                location_region="South Zone",
                image_path="uploads/test.jpg",
                model_prediction="Potato Late Blight",
                confidence=0.60,
                status="Needs expert review",
                created_at=now - timedelta(hours=i*2)
            )
            db.session.add(obs)
        db.session.commit()

        # Check and trigger alerts
        alerts = check_and_trigger_outbreak_alerts(threshold=3)
        assert len(alerts) >= 1
        alert = OutbreakAlert.query.filter_by(region="South Zone", crop="Potato").first()
        assert alert is not None
        assert alert.incident_count >= 3
        assert alert.severity in ["High", "Critical"]
        assert alert.status == "Active"
