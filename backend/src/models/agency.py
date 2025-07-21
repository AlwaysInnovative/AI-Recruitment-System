from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class RecruitmentAgency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    commission_rate = db.Column(db.Float, nullable=False)  # Percentage (e.g., 15.0 for 15%)
    payment_terms = db.Column(db.String(200), nullable=True)  # e.g., "30 days after start date"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<RecruitmentAgency {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_person': self.contact_person,
            'email': self.email,
            'phone': self.phone,
            'commission_rate': self.commission_rate,
            'payment_terms': self.payment_terms,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Commission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    agency_id = db.Column(db.Integer, db.ForeignKey('recruitment_agency.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    payment_date = db.Column(db.DateTime, nullable=True)
    transaction_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    application = db.relationship('Application', backref=db.backref('commissions', lazy=True))
    agency = db.relationship('RecruitmentAgency', backref=db.backref('commissions', lazy=True))
    
    def __repr__(self):
        return f'<Commission {self.id}: ${self.amount} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'agency_id': self.agency_id,
            'amount': self.amount,
            'status': self.status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'transaction_id': self.transaction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

