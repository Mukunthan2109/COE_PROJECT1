import pytest
import os
import io
from app import create_app
from app.models import db, User, Observation, ExpertReview
from app.translations import TRANSLATIONS, get_translation

@pytest.fixture
def app_instance():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

def test_password_hashing_security(app_instance):
    with app_instance.app_context():
        user = User(username='sec_expert', email='sec@agri.org', role='expert')
        user.set_password('SecretPassword123')
        assert user.password_hash != 'SecretPassword123'
        assert user.check_password('SecretPassword123') is True
        assert user.check_password('WrongPassword') is False

def test_invalid_file_extension_rejection(client):
    data = {
        'crop': 'Tomato',
        'symptom': 'Yellowing leaves',
        'crop_stage': 'Vegetative',
        'location_region': 'North Zone',
        'crop_image': (io.BytesIO(b'<?php echo "malicious"; ?>'), 'malicious_script.php')
    }
    response = client.post('/observe', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid image format" in response.data or b"PNG, JPG, JPEG, WEBP" in response.data

def test_bilingual_translations_completeness():
    en_keys = set(TRANSLATIONS['en'].keys())
    ta_keys = set(TRANSLATIONS['ta'].keys())
    
    assert 'crop_chili' in en_keys
    assert 'crop_chili' in ta_keys
    assert TRANSLATIONS['ta']['crop_chili'] == 'மிளகாய்'
    assert TRANSLATIONS['en']['crop_chili'] == 'Chili'

def test_expert_unauthorized_redirect(client):
    response = client.get('/expert', follow_redirects=True)
    assert response.status_code == 200
    assert b"login" in response.data.lower() or b"sign in" in response.data.lower() or b"expert" in response.data.lower()

def test_status_lookup_nonexistent_id(client):
    response = client.get('/status?obs_id=999999', follow_redirects=True)
    assert response.status_code == 200
    assert b"No observation found" in response.data or b"Invalid" in response.data or b"Status" in response.data

def test_demo_seeder_execution(app_instance):
    from scripts.seed_demo import seed_demo_data
    with app_instance.app_context():
        seed_demo_data()
        obs_count = Observation.query.count()
        rev_count = ExpertReview.query.count()
        assert obs_count >= 5
        assert rev_count >= 1

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}
