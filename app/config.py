import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-farmer-app-2026-full')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "farmer_app.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    HEATMAP_FOLDER = os.path.join(BASE_DIR, 'static', 'heatmaps')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', 0.70))
    OUTBREAK_ALERT_THRESHOLD = int(os.environ.get('OUTBREAK_ALERT_THRESHOLD', 3)) # Alert if >=3 cases in 48h
    MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'ml', 'saved_model'))
