from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='applied')  # applied, reviewed, interviewed, offered, hired, rejected
    matching_score = db.Column(db.Float, nullable=True)
    right_to_representation_status = db.Column(db.String(20), default='pending')  # pending, sent, signed
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    candidate = db.relationship('Candidate', backref=db.backref('applications', lazy=True))
    
    def __repr__(self):
        return f'<Application {self.id}: Job {self.job_id} - Candidate {self.candidate_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'candidate_id': self.candidate_id,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'status': self.status,
            'matching_score': self.matching_score,
            'right_to_representation_status': self.right_to_representation_status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_details(self):
        """Return application with job and candidate details"""
        result = self.to_dict()
        if self.job:
            result['job'] = self.job.to_dict()
        if self.candidate:
            result['candidate'] = self.candidate.to_dict()
        return result

