from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class CommunicationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # email, sms
    subject = db.Column(db.String(200), nullable=True)  # For emails
    body = db.Column(db.Text, nullable=False)
    recipient = db.Column(db.String(120), nullable=False)  # Email or phone number
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='sent')  # sent, failed, delivered, opened
    provider_response = db.Column(db.Text, nullable=True)  # Response from email/SMS provider
    
    # Relationship
    application = db.relationship('Application', backref=db.backref('communications', lazy=True))
    
    def __repr__(self):
        return f'<CommunicationLog {self.id}: {self.type} to {self.recipient}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'type': self.type,
            'subject': self.subject,
            'body': self.body,
            'recipient': self.recipient,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'status': self.status,
            'provider_response': self.provider_response
        }

