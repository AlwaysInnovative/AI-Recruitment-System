from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db
import json

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    linkedin_profile = db.Column(db.String(200), nullable=True)
    total_experience_years = db.Column(db.Float, nullable=True)
    education = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)  # JSON string of skills array
    parsed_cv_text = db.Column(db.Text, nullable=True)
    cv_file_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Candidate {self.first_name} {self.last_name}>'
    
    def get_skills_list(self):
        """Convert skills JSON string to list"""
        if self.skills:
            try:
                return json.loads(self.skills)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_skills_list(self, skills_list):
        """Convert skills list to JSON string"""
        self.skills = json.dumps(skills_list) if skills_list else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'linkedin_profile': self.linkedin_profile,
            'total_experience_years': self.total_experience_years,
            'education': self.education,
            'skills': self.get_skills_list(),
            'parsed_cv_text': self.parsed_cv_text,
            'cv_file_path': self.cv_file_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

