import pytest
from app import create_app
from app.models import db, User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_user_registration(client):
    res = client.post('/register', data={
        'username': 'newfarmer_unique',
        'email': 'newfarmer_unique@example.com',
        'password': 'password123',
        'role': 'farmer',
        'region': 'North Zone'
    }, follow_redirects=True)

    assert res.status_code == 200
    with client.application.app_context():
        user = User.query.filter_by(username='newfarmer_unique').first()
        assert user is not None
        assert user.role == 'farmer'
        assert user.check_password('password123') is True

def test_user_login_logout(client):
    with client.application.app_context():
        user = User(username='testexpert_login', email='testexpert_login@example.com', role='expert', region='South Zone')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

    res_login = client.post('/login', data={
        'username': 'testexpert_login',
        'password': 'password123'
    }, follow_redirects=True)
    assert res_login.status_code == 200
    assert b"Welcome back, testexpert_login" in res_login.data

    res_logout = client.get('/logout', follow_redirects=True)
    assert res_logout.status_code == 200
    assert b"Logged out successfully" in res_logout.data

def test_invalid_login(client):
    res = client.post('/login', data={
        'username': 'nonexistent_user',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b"Invalid username or password" in res.data
