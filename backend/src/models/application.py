from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db
from sqlalchemy.dialects.postgresql import JSONB  # For PostgreSQL users

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='applied')  # applied, reviewed, interviewed, offered, hired, rejected
    matching_score = db.Column(db.Float, nullable=True)
    
    # Enhanced right to represent fields
    right_to_represent = db.Column(JSONB, default={
        'status': 'pending',  # pending, sent, signed, declined
        'sent_at': None,
        'signed_at': None,
        'document_url': None,
        'declined_reason': None
    })
    
    # CV/Resume tracking
    cv_data = db.Column(JSONB, default={
        'original_filename': None,
        'storage_path': None,
        'text_content': None,
        'parsed_data': None  # Stores structured data from parsing
    })
    
    # AI matching details
    matching_details = db.Column(JSONB, default={
        'skills_match': None,
        'experience_match': None,
        'education_match': None,
        'keyword_matches': None,
        'last_calculated': None
    })
    
    # Communication history
    communication_history = db.Column(JSONB, default=[])
    
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    candidate = db.relationship('Candidate', backref=db.backref('applications', lazy=True))
    commissions = db.relationship('Commission', backref='application', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Application {self.id}: Job {self.job_id} - Candidate {self.candidate_id}>'
    
    def to_dict(self):
        """Basic serialization with core fields"""
        return {
            'id': self.id,
            'job_id': self.job_id,
            'candidate_id': self.candidate_id,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'status': self.status,
            'matching_score': self.matching_score,
            'right_to_represent': self.right_to_represent,
            'cv_data': self.cv_data,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_details(self):
        """Comprehensive serialization with related objects and AI details"""
        result = self.to_dict()
        result['matching_details'] = self.matching_details
        result['communication_history'] = self.communication_history
        
        if self.job:
            result['job'] = self.job.to_dict()
        if self.candidate:
            result['candidate'] = self.candidate.to_dict()
        if self.commissions:
            result['commissions'] = [c.to_dict() for c in self.commissions]
        
        return result
    
    def update_matching_score(self, score, details):
        """Update AI matching results"""
        self.matching_score = score
        self.matching_details = {
            **details,
            'last_calculated': datetime.utcnow().isoformat()
        }
        db.session.commit()
        return self
    
    def send_right_to_represent(self, document_url):
        """Mark right to represent as sent"""
        self.right_to_represent = {
            'status': 'sent',
            'sent_at': datetime.utcnow().isoformat(),
            'document_url': document_url,
            'signed_at': None,
            'declined_reason': None
        }
        self.add_communication_event(
            type='right_to_represent',
            action='sent',
            details={'document_url': document_url}
        )
        db.session.commit()
        return self
    
    def add_communication_event(self, event_type, action, details=None):
        """Track communication history"""
        if not self.communication_history:
            self.communication_history = []
            
        self.communication_history.append({
            'type': event_type,
            'action': action,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {}
        })
        db.session.commit()
        return self
    
    def calculate_commission(self):
        """Calculate potential commission if application results in hire"""
        if self.status != 'hired':
            return None
            
        # Default commission rate (can be overridden by agency relationship)
        commission_rate = 0.15  # 15%
        
        # Calculate based on job salary if available
        if self.job and self.job.salary:
            return {
                'amount': round(self.job.salary * commission_rate, 2),
                'currency': self.job.salary_currency or 'USD',
                'rate': commission_rate
            }
        return None
