from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), default='farmer', nullable=False) # 'farmer', 'expert', 'qa_manager'
    region = db.Column(db.String(100), default='North Zone', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    observations = db.relationship('Observation', backref='farmer', lazy=True)
    expert_reviews = db.relationship('ExpertReview', backref='expert', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'region': self.region
        }


class Observation(db.Model):
    __tablename__ = 'observations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    crop = db.Column(db.String(50), nullable=False)
    symptom = db.Column(db.String(100), nullable=False)
    crop_stage = db.Column(db.String(50), nullable=False)
    location_region = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    heatmap_path = db.Column(db.String(255), nullable=True) # Grad-CAM visual explainability heatmap
    observation_notes = db.Column(db.Text, nullable=True)
    observation_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ML / DL Triage Results
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
            'user_id': self.user_id,
            'crop': self.crop,
            'symptom': self.symptom,
            'crop_stage': self.crop_stage,
            'location_region': self.location_region,
            'image_path': self.image_path,
            'heatmap_path': self.heatmap_path,
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
    expert_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    expert_label = db.Column(db.String(100), nullable=False)
    expert_status = db.Column(db.String(50), nullable=False) # 'Confirmed', 'Corrected', 'Uncertain'
    expert_comment = db.Column(db.Text, nullable=True)
    review_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    time_to_review_seconds = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'observation_id': self.observation_id,
            'expert_user_id': self.expert_user_id,
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


class BatchProcurement(db.Model):
    __tablename__ = 'batch_procurements'

    id = db.Column(db.Integer, primary_key=True)
    batch_code = db.Column(db.String(64), unique=True, nullable=False)
    crop = db.Column(db.String(50), nullable=False)
    supplier_region = db.Column(db.String(100), nullable=False)
    total_weight_kg = db.Column(db.Float, nullable=False)
    sample_size_count = db.Column(db.Integer, nullable=False)
    diseased_sample_count = db.Column(db.Integer, nullable=False)
    defect_rate_percent = db.Column(db.Float, nullable=False)
    quality_grade = db.Column(db.String(32), nullable=False) # 'Grade A', 'Grade B', 'Grade C', 'REJECT'
    intake_status = db.Column(db.String(32), nullable=False) # 'Approved', 'Conditional', 'Rejected'
    inspection_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'batch_code': self.batch_code,
            'crop': self.crop,
            'supplier_region': self.supplier_region,
            'total_weight_kg': self.total_weight_kg,
            'sample_size_count': self.sample_size_count,
            'diseased_sample_count': self.diseased_sample_count,
            'defect_rate_percent': round(self.defect_rate_percent, 1),
            'quality_grade': self.quality_grade,
            'intake_status': self.intake_status,
            'inspection_notes': self.inspection_notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class OutbreakAlert(db.Model):
    __tablename__ = 'outbreak_alerts'

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)
    crop = db.Column(db.String(50), nullable=False)
    disease = db.Column(db.String(100), nullable=False)
    incident_count = db.Column(db.Integer, nullable=False)
    severity = db.Column(db.String(32), nullable=False) # 'Low', 'Medium', 'High', 'Critical'
    status = db.Column(db.String(32), default='Active', nullable=False) # 'Active', 'Resolved'
    alert_message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'region': self.region,
            'crop': self.crop,
            'disease': self.disease,
            'incident_count': self.incident_count,
            'severity': self.severity,
            'status': self.status,
            'alert_message': self.alert_message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


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
