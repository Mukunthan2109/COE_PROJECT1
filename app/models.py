from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Observation(db.Model):
    __tablename__ = 'observations'

    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50), nullable=False)
    symptom = db.Column(db.String(100), nullable=False)
    crop_stage = db.Column(db.String(50), nullable=False)
    location_region = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    observation_notes = db.Column(db.Text, nullable=True)
    observation_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ML Triage Results
    model_prediction = db.Column(db.String(100), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    explainability_notes = db.Column(db.Text, nullable=True)
    
    # Status: 'Initial screening result', 'Needs expert review', 'Reviewed by expert'
    status = db.Column(db.String(50), default='Needs expert review', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    expert_review = db.relationship('ExpertReview', backref='observation', uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'crop': self.crop,
            'symptom': self.symptom,
            'crop_stage': self.crop_stage,
            'location_region': self.location_region,
            'image_path': self.image_path,
            'observation_notes': self.observation_notes,
            'observation_timestamp': self.observation_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'model_prediction': self.model_prediction,
            'confidence': round(self.confidence * 100, 1) if self.confidence else None,
            'explainability_notes': self.explainability_notes,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class ExpertReview(db.Model):
    __tablename__ = 'expert_reviews'

    id = db.Column(db.Integer, primary_key=True)
    observation_id = db.Column(db.Integer, db.ForeignKey('observations.id'), nullable=False)
    expert_label = db.Column(db.String(100), nullable=False)
    expert_status = db.Column(db.String(50), nullable=False) # 'Confirmed', 'Corrected', 'Uncertain'
    expert_comment = db.Column(db.Text, nullable=True)
    review_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    time_to_review_seconds = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'observation_id': self.observation_id,
            'expert_label': self.expert_label,
            'expert_status': self.expert_status,
            'expert_comment': self.expert_comment,
            'review_timestamp': self.review_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'time_to_review_seconds': self.time_to_review_seconds,
            'time_to_review_formatted': self.format_time_to_review()
        }

    def format_time_to_review(self):
        total_seconds = int(self.time_to_review_seconds)
        if total_seconds < 60:
            return f"{total_seconds} sec"
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        if minutes < 60:
            return f"{minutes}m {seconds}s"
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m"


class DatasetMetadata(db.Model):
    __tablename__ = 'dataset_metadata'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(50), unique=True, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    crop = db.Column(db.String(50), nullable=False)
    symptom = db.Column(db.String(100), nullable=False)
    disease_label = db.Column(db.String(100), nullable=False)
    location_region = db.Column(db.String(100), nullable=False)
    crop_stage = db.Column(db.String(50), nullable=False)
    source_type = db.Column(db.String(50), nullable=False) # 'project_created', 'public_licensed'
    expert_validation = db.Column(db.String(50), default='pending') # 'pending', 'verified'
    license_or_source_note = db.Column(db.String(255), nullable=True)
