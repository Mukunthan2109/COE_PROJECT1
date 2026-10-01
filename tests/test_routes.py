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

    # Post expert review with valid status choice
    review_data = {
        'expert_label': 'Tomato Leaf Spot (Confirmed)',
        'expert_status': 'Validated (Confirmed)',
        'expert_comment': 'Confirmed diagnosis. Apply organic copper spray.'
    }
    
    res = client.post(f'/expert/review/{obs_id}', data=review_data, follow_redirects=True)
    assert res.status_code == 200

    with client.application.app_context():
        updated_obs = db.session.get(Observation, obs_id)
        assert updated_obs.status == 'Reviewed by expert'
        assert updated_obs.expert_review is not None
        assert updated_obs.expert_review.expert_label == 'Tomato Leaf Spot (Confirmed)'
        assert updated_obs.expert_review.expert_status == 'Validated (Confirmed)'
        assert updated_obs.expert_review.time_to_review_seconds >= 0.0

def test_expert_review_invalid_status_rejection(client):
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

    # Post expert review with missing/invalid status
    review_data = {
        'expert_label': 'Tomato Leaf Spot',
        'expert_status': '',
        'expert_comment': 'Missing status'
    }
    res = client.post(f'/expert/review/{obs_id}', data=review_data, follow_redirects=True)
    assert b"Please select a valid expert review status" in res.data

def test_duplicate_submission_detection(client):
    img_byte_arr = io.BytesIO()
    img_arr = np.random.randint(50, 200, (200, 200, 3), dtype=np.uint8)
    Image.fromarray(img_arr).save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    img_bytes = img_byte_arr.read()

    data1 = {
        'crop': 'Tomato',
        'symptom': 'Healthy',
        'crop_stage': 'Vegetative',
        'location_region': 'North Zone',
        'crop_image': (io.BytesIO(img_bytes), 'same_leaf.jpg')
    }
    res1 = client.post('/observe', data=data1, content_type='multipart/form-data', follow_redirects=True)
    assert res1.status_code == 200

    data2 = {
        'crop': 'Tomato',
        'symptom': 'Healthy',
        'crop_stage': 'Vegetative',
        'location_region': 'North Zone',
        'crop_image': (io.BytesIO(img_bytes), 'same_leaf.jpg')
    }
    res2 = client.post('/observe', data=data2, content_type='multipart/form-data', follow_redirects=True)
    assert res2.status_code == 200
    assert b"Duplicate Image Detected" in res2.data

def test_observation_detail_route(client):
    with client.application.app_context():
        obs = Observation(
            crop="Potato",
            symptom="Early Blight",
            crop_stage="Vegetative",
            location_region="North Zone",
            image_path="uploads/demo.jpg",
            model_prediction="Potato Early Blight",
            confidence=0.92,
            risk_level="High",
            status="Initial screening result"
        )
        db.session.add(obs)
        db.session.commit()
        obs_id = obs.id

    res = client.get(f'/observation/{obs_id}')
    assert res.status_code == 200
    assert b"Observation Record Details" in res.data
    assert b"High Risk" in res.data

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

def test_empty_database_history_state(client):
    with client.application.app_context():
        Observation.query.delete()
        db.session.commit()
    res = client.get('/history')
    assert res.status_code == 200
    assert b"No observations submitted yet." in res.data

def test_empty_database_expert_portal_state(client):
    with client.application.app_context():
        Observation.query.delete()
        db.session.commit()
    res = client.get('/expert')
    assert res.status_code == 200
    assert b"No pending expert reviews." in res.data

def test_evaluation_page_12_class(client):
    res = client.get('/evaluation')
    assert res.status_code == 200
    assert b"Test Accuracy (12-Class)" in res.data



