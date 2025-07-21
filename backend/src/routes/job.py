from flask import Blueprint, jsonify, request
from src.models.job import Job, db
from src.models.user import User

job_bp = Blueprint('job', __name__)

@job_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs with optional filtering"""
    status = request.args.get('status')
    hiring_manager_id = request.args.get('hiring_manager_id')
    
    query = Job.query
    
    if status:
        query = query.filter(Job.status == status)
    if hiring_manager_id:
        query = query.filter(Job.hiring_manager_id == hiring_manager_id)
    
    jobs = query.all()
    return jsonify([job.to_dict() for job in jobs])

@job_bp.route('/jobs', methods=['POST'])
def create_job():
    """Create a new job posting"""
    data = request.json
    
    # Validate required fields
    required_fields = ['title', 'description', 'requirements', 'hiring_manager_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Verify hiring manager exists
    hiring_manager = User.query.get(data['hiring_manager_id'])
    if not hiring_manager:
        return jsonify({'error': 'Hiring manager not found'}), 404
    
    job = Job(
        title=data['title'],
        description=data['description'],
        requirements=data['requirements'],
        responsibilities=data.get('responsibilities'),
        location=data.get('location'),
        salary_range=data.get('salary_range'),
        hiring_manager_id=data['hiring_manager_id']
    )
    
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_dict()), 201

@job_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job by ID"""
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict())

@job_bp.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Update an existing job"""
    job = Job.query.get_or_404(job_id)
    data = request.json
    
    # Update fields if provided
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.requirements = data.get('requirements', job.requirements)
    job.responsibilities = data.get('responsibilities', job.responsibilities)
    job.location = data.get('location', job.location)
    job.salary_range = data.get('salary_range', job.salary_range)
    job.status = data.get('status', job.status)
    
    db.session.commit()
    return jsonify(job.to_dict())

@job_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job posting"""
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return '', 204

@job_bp.route('/jobs/<int:job_id>/applications', methods=['GET'])
def get_job_applications(job_id):
    """Get all applications for a specific job"""
    job = Job.query.get_or_404(job_id)
    applications = [app.to_dict_with_details() for app in job.applications]
    return jsonify(applications)

