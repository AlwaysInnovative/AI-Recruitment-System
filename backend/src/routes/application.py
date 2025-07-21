from flask import Blueprint, jsonify, request
from src.models.application import Application, db
from src.models.job import Job
from src.models.candidate import Candidate

application_bp = Blueprint('application', __name__)

@application_bp.route('/applications', methods=['GET'])
def get_applications():
    """Get all applications with optional filtering"""
    job_id = request.args.get('job_id')
    candidate_id = request.args.get('candidate_id')
    status = request.args.get('status')
    
    query = Application.query
    
    if job_id:
        query = query.filter(Application.job_id == job_id)
    if candidate_id:
        query = query.filter(Application.candidate_id == candidate_id)
    if status:
        query = query.filter(Application.status == status)
    
    applications = query.all()
    return jsonify([app.to_dict_with_details() for app in applications])

@application_bp.route('/applications', methods=['POST'])
def create_application():
    """Create a new job application"""
    data = request.json
    
    # Validate required fields
    required_fields = ['job_id', 'candidate_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Verify job and candidate exist
    job = Job.query.get(data['job_id'])
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    candidate = Candidate.query.get(data['candidate_id'])
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    # Check if application already exists
    existing_application = Application.query.filter_by(
        job_id=data['job_id'],
        candidate_id=data['candidate_id']
    ).first()
    if existing_application:
        return jsonify({'error': 'Application already exists for this job and candidate'}), 409
    
    application = Application(
        job_id=data['job_id'],
        candidate_id=data['candidate_id'],
        status=data.get('status', 'applied'),
        matching_score=data.get('matching_score'),
        notes=data.get('notes')
    )
    
    db.session.add(application)
    db.session.commit()
    return jsonify(application.to_dict_with_details()), 201

@application_bp.route('/applications/<int:application_id>', methods=['GET'])
def get_application(application_id):
    """Get a specific application by ID"""
    application = Application.query.get_or_404(application_id)
    return jsonify(application.to_dict_with_details())

@application_bp.route('/applications/<int:application_id>', methods=['PUT'])
def update_application(application_id):
    """Update an existing application"""
    application = Application.query.get_or_404(application_id)
    data = request.json
    
    # Update fields if provided
    application.status = data.get('status', application.status)
    application.matching_score = data.get('matching_score', application.matching_score)
    application.right_to_representation_status = data.get('right_to_representation_status', application.right_to_representation_status)
    application.notes = data.get('notes', application.notes)
    
    db.session.commit()
    return jsonify(application.to_dict_with_details())

@application_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
def update_application_status(application_id):
    """Update application status specifically"""
    application = Application.query.get_or_404(application_id)
    data = request.json
    
    if 'status' not in data:
        return jsonify({'error': 'Missing required field: status'}), 400
    
    valid_statuses = ['applied', 'reviewed', 'interviewed', 'offered', 'hired', 'rejected']
    if data['status'] not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
    
    application.status = data['status']
    db.session.commit()
    
    return jsonify(application.to_dict_with_details())

@application_bp.route('/applications/<int:application_id>', methods=['DELETE'])
def delete_application(application_id):
    """Delete an application"""
    application = Application.query.get_or_404(application_id)
    db.session.delete(application)
    db.session.commit()
    return '', 204

