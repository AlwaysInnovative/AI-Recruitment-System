from flask import Blueprint, jsonify, request
from src.models.agency import RecruitmentAgency, Commission, db
from src.models.application import Application

agency_bp = Blueprint('agency', __name__)

# Recruitment Agency routes
@agency_bp.route('/agencies', methods=['GET'])
def get_agencies():
    """Get all recruitment agencies"""
    agencies = RecruitmentAgency.query.all()
    return jsonify([agency.to_dict() for agency in agencies])

@agency_bp.route('/agencies', methods=['POST'])
def create_agency():
    """Create a new recruitment agency"""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'contact_person', 'email', 'commission_rate']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    agency = RecruitmentAgency(
        name=data['name'],
        contact_person=data['contact_person'],
        email=data['email'],
        phone=data.get('phone'),
        commission_rate=data['commission_rate'],
        payment_terms=data.get('payment_terms')
    )
    
    db.session.add(agency)
    db.session.commit()
    return jsonify(agency.to_dict()), 201

@agency_bp.route('/agencies/<int:agency_id>', methods=['GET'])
def get_agency(agency_id):
    """Get a specific agency by ID"""
    agency = RecruitmentAgency.query.get_or_404(agency_id)
    return jsonify(agency.to_dict())

@agency_bp.route('/agencies/<int:agency_id>', methods=['PUT'])
def update_agency(agency_id):
    """Update an existing agency"""
    agency = RecruitmentAgency.query.get_or_404(agency_id)
    data = request.json
    
    # Update fields if provided
    agency.name = data.get('name', agency.name)
    agency.contact_person = data.get('contact_person', agency.contact_person)
    agency.email = data.get('email', agency.email)
    agency.phone = data.get('phone', agency.phone)
    agency.commission_rate = data.get('commission_rate', agency.commission_rate)
    agency.payment_terms = data.get('payment_terms', agency.payment_terms)
    
    db.session.commit()
    return jsonify(agency.to_dict())

@agency_bp.route('/agencies/<int:agency_id>', methods=['DELETE'])
def delete_agency(agency_id):
    """Delete an agency"""
    agency = RecruitmentAgency.query.get_or_404(agency_id)
    db.session.delete(agency)
    db.session.commit()
    return '', 204

# Commission routes
@agency_bp.route('/commissions', methods=['GET'])
def get_commissions():
    """Get all commissions with optional filtering"""
    agency_id = request.args.get('agency_id')
    status = request.args.get('status')
    
    query = Commission.query
    
    if agency_id:
        query = query.filter(Commission.agency_id == agency_id)
    if status:
        query = query.filter(Commission.status == status)
    
    commissions = query.all()
    return jsonify([commission.to_dict() for commission in commissions])

@agency_bp.route('/commissions', methods=['POST'])
def create_commission():
    """Create a new commission record"""
    data = request.json
    
    # Validate required fields
    required_fields = ['application_id', 'agency_id', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Verify application and agency exist
    application = Application.query.get(data['application_id'])
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    agency = RecruitmentAgency.query.get(data['agency_id'])
    if not agency:
        return jsonify({'error': 'Agency not found'}), 404
    
    commission = Commission(
        application_id=data['application_id'],
        agency_id=data['agency_id'],
        amount=data['amount'],
        status=data.get('status', 'pending')
    )
    
    db.session.add(commission)
    db.session.commit()
    return jsonify(commission.to_dict()), 201

@agency_bp.route('/commissions/<int:commission_id>', methods=['GET'])
def get_commission(commission_id):
    """Get a specific commission by ID"""
    commission = Commission.query.get_or_404(commission_id)
    return jsonify(commission.to_dict())

@agency_bp.route('/commissions/<int:commission_id>', methods=['PUT'])
def update_commission(commission_id):
    """Update an existing commission"""
    commission = Commission.query.get_or_404(commission_id)
    data = request.json
    
    # Update fields if provided
    commission.amount = data.get('amount', commission.amount)
    commission.status = data.get('status', commission.status)
    commission.transaction_id = data.get('transaction_id', commission.transaction_id)
    
    # Update payment_date if status is being set to 'paid'
    if data.get('status') == 'paid' and commission.status != 'paid':
        from datetime import datetime
        commission.payment_date = datetime.utcnow()
    
    db.session.commit()
    return jsonify(commission.to_dict())

@agency_bp.route('/commissions/<int:commission_id>/pay', methods=['POST'])
def pay_commission(commission_id):
    """Initiate payment for a commission"""
    commission = Commission.query.get_or_404(commission_id)
    
    if commission.status == 'paid':
        return jsonify({'error': 'Commission already paid'}), 400
    
    # In a real implementation, this would integrate with a payment gateway
    # For now, we'll simulate the payment process
    data = request.json
    transaction_id = data.get('transaction_id', f'TXN_{commission_id}_{int(datetime.utcnow().timestamp())}')
    
    commission.status = 'paid'
    commission.transaction_id = transaction_id
    from datetime import datetime
    commission.payment_date = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Payment initiated successfully',
        'commission': commission.to_dict()
    })

