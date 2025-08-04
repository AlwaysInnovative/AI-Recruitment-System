from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db
from sqlalchemy.dialects.postgresql import JSONB

class Commission(db.Model):
    __tablename__ = 'commissions'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'), nullable=False)
    
    # Payment details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='pending')  # pending, approved, processing, paid, failed, cancelled
    payment_method = db.Column(db.String(50))  # stripe, bank_transfer, etc.
    
    # Dates
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    processed_at = db.Column(db.DateTime)
    paid_at = db.Column(db.DateTime)
    
    # References
    payment_reference = db.Column(db.String(100))  # Transaction ID from payment processor
    invoice_number = db.Column(db.String(50))
    
    # Metadata
    metadata = db.Column(JSONB)  # For storing additional data like payment gateway response
    
    # Relationships
    application = db.relationship('Application', backref=db.backref('commissions', lazy=True))
    agency = db.relationship('Agency', backref=db.backref('commissions', lazy=True))
    
    def __repr__(self):
        return f'<Commission {self.id}: ${self.amount} {self.currency} for App {self.application_id}>'
    
    def to_dict(self):
        """Basic serialization"""
        return {
            'id': self.id,
            'application_id': self.application_id,
            'agency_id': self.agency_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'calculated_at': self.calculated_at.isoformat() if self.calculated_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'payment_reference': self.payment_reference,
            'invoice_number': self.invoice_number
        }
    
    def to_dict_with_details(self):
        """Comprehensive serialization with related objects"""
        result = self.to_dict()
        if self.application:
            result['application'] = {
                'id': self.application.id,
                'job_title': self.application.job.title if self.application.job else None,
                'candidate_name': self.application.candidate.full_name if self.application.candidate else None
            }
        if self.agency:
            result['agency'] = {
                'id': self.agency.id,
                'name': self.agency.name,
                'contact_email': self.agency.contact_email
            }
        return result
    
    def calculate(self, commission_rate=None):
        """
        Calculate commission amount based on application salary
        Args:
            commission_rate: Optional override of default agency rate
        """
        if not self.application or self.application.status != 'hired':
            raise ValueError("Commission can only be calculated for hired applications")
        
        if not self.application.job or not self.application.job.salary:
            raise ValueError("Job salary information missing")
        
        rate = commission_rate or self.agency.commission_rate
        self.amount = round(self.application.job.salary * rate, 2)
        self.calculated_at = datetime.utcnow()
        self.status = 'pending'
        return self
    
    def approve(self, approved_by):
        """Mark commission as approved"""
        self.status = 'approved'
        self.approved_at = datetime.utcnow()
        self.metadata = {
            **(self.metadata or {}),
            'approved_by': approved_by,
            'approval_date': datetime.utcnow().isoformat()
        }
        return self
    
    def process_payment(self, payment_method='stripe', **kwargs):
        """
        Initiate commission payment
        Args:
            payment_method: Payment processor to use
            kwargs: Processor-specific parameters
        """
        if self.status != 'approved':
            raise ValueError("Commission must be approved before payment processing")
        
        self.payment_method = payment_method
        self.processed_at = datetime.utcnow()
        self.status = 'processing'
        
        # Store payment processor metadata
        self.metadata = {
            **(self.metadata or {}),
            'payment_processor': payment_method,
            'processing_started_at': datetime.utcnow().isoformat(),
            'processor_params': kwargs
        }
        
        # In a real implementation, you would call the payment processor API here
        # This is just a placeholder for the actual integration
        try:
            # Example for Stripe:
            if payment_method == 'stripe':
                payment_result = self._process_stripe_payment(**kwargs)
                self.payment_reference = payment_result['id']
                self.status = 'paid'
                self.paid_at = datetime.utcnow()
            # Add other payment methods as needed
            
            db.session.commit()
            return True
        except Exception as e:
            self.status = 'failed'
            self.metadata['error'] = str(e)
            db.session.commit()
            raise
    
    def _process_stripe_payment(self, stripe_account_id, **kwargs):
        """Example Stripe payment processing"""
        # In a real implementation, this would call the Stripe API
        # This is just a mock implementation
        return {
            'id': f'ch_{datetime.now().timestamp()}',
            'status': 'succeeded',
            'amount': self.amount,
            'currency': self.currency
        }
    
    def generate_invoice(self):
        """Generate invoice document for this commission"""
        if not self.invoice_number:
            self.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{self.id}"
        
        # In a real implementation, this would generate a PDF invoice
        invoice_data = {
            'invoice_number': self.invoice_number,
            'date': datetime.utcnow().date().isoformat(),
            'agency': {
                'name': self.agency.name,
                'address': self.agency.address,
                'tax_id': self.agency.tax_id
            },
            'items': [{
                'description': f"Commission for placement of {self.application.candidate.full_name}",
                'amount': self.amount,
                'currency': self.currency
            }],
            'total': self.amount,
            'currency': self.currency,
            'payment_terms': self.agency.payment_terms or 'NET 30'
        }
        
        self.metadata = {
            **(self.metadata or {}),
            'invoice_generated_at': datetime.utcnow().isoformat(),
            'invoice_data': invoice_data
        }
        
        return invoice_data
