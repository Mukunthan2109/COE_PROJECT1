import os
import io
import pytest
import numpy as np
from PIL import Image
from app import create_app
from app.models import db, Observation, ExpertReview

@pytest.fixture
def client(tmp_path):
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['UPLOAD_FOLDER'] = str(tmp_path)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

def test_home_page(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"AgriShield" in res.data

def test_observe_get(client):
    res = client.get('/observe')
    assert res.status_code == 200
    assert b"Observation" in res.data or b"Step 1" in res.data

def test_observe_post_valid(client):
    # Generate valid in-memory image
    img_byte_arr = io.BytesIO()
    img_arr = np.random.randint(50, 200, (200, 200, 3), dtype=np.uint8)
    Image.fromarray(img_arr).save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    data = {
        'crop': 'Tomato',
        'symptom': 'Healthy',
        'crop_stage': 'Vegetative',
        'location_region': 'North Zone',
        'observation_notes': 'Test submission',
        'crop_image': (img_byte_arr, 'test_tomato.jpg')
    }
    
    res = client.post('/observe', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert res.status_code == 200
    assert b"Initial Screening Result" in res.data or b"Observation ID:" in res.data

def test_expert_review_workflow(client):
    # Seed observation in DB
    with client.application.app_context():
        obs = Observation(
            crop="Tomato",
            symptom="Leaf Spot",
            crop_stage="Flowering",
            location_region="South Zone",
            image_path="uploads/test.jpg",
            model_prediction="Tomato Leaf Spot",
            confidence=0.50,
            status="Needs expert review"
        )
        db.session.add(obs)
        db.session.commit()
        obs_id = obs.id

    # Post expert review
    review_data = {
        'expert_label': 'Tomato Leaf Spot (Confirmed)',
        'expert_status': 'Confirmed',
        'expert_comment': 'Confirmed diagnosis. Apply organic copper spray.'
    }
    
    res = client.post(f'/expert/review/{obs_id}', data=review_data, follow_redirects=True)
    assert res.status_code == 200

    with client.application.app_context():
        updated_obs = db.session.get(Observation, obs_id)
        assert updated_obs.status == 'Reviewed by expert'
        assert updated_obs.expert_review is not None
        assert updated_obs.expert_review.expert_label == 'Tomato Leaf Spot (Confirmed)'
        assert updated_obs.expert_review.time_to_review_seconds >= 0.0

def test_scan_workflow(client):
    res_get = client.get('/scan')
    assert res_get.status_code == 200
    assert b"Instant AI Crop Disease Scanner" in res_get.data

    img_byte_arr = io.BytesIO()
    img_arr = np.random.randint(50, 200, (200, 200, 3), dtype=np.uint8)
    Image.fromarray(img_arr).save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    data = {
        'crop_image': (img_byte_arr, 'scan_test.jpg')
    }
    
    res_post = client.post('/scan', data=data, content_type='multipart/form-data')
    assert res_post.status_code == 200
    assert b"AI Diagnostic Analysis Result" in res_post.data

def test_analyze_image_api(client):
    img_byte_arr = io.BytesIO()
    img_arr = np.random.randint(50, 200, (200, 200, 3), dtype=np.uint8)
    Image.fromarray(img_arr).save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    data = {
        'crop_image': (img_byte_arr, 'api_test.jpg')
    }

    res = client.post('/api/analyze-image', data=data, content_type='multipart/form-data')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['success'] is True
    assert 'prediction' in json_data
    assert 'detected_crop' in json_data

