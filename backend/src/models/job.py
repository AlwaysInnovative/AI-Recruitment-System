from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    responsibilities = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    salary_range = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='open')  # open, closed, filled
    hiring_manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    hiring_manager = db.relationship('User', backref=db.backref('jobs', lazy=True))
    
    def __repr__(self):
        return f'<Job {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'responsibilities': self.responsibilities,
            'location': self.location,
            'salary_range': self.salary_range,
            'status': self.status,
            'hiring_manager_id': self.hiring_manager_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

