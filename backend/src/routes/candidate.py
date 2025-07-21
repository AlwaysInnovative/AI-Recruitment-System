from flask import Blueprint, jsonify, request
from src.models.candidate import Candidate, db
import json

candidate_bp = Blueprint('candidate', __name__)

@candidate_bp.route('/candidates', methods=['GET'])
def get_candidates():
    """Get all candidates with optional filtering"""
    email = request.args.get('email')
    skills = request.args.get('skills')  # Comma-separated skills
    
    query = Candidate.query
    
    if email:
        query = query.filter(Candidate.email.ilike(f'%{email}%'))
    
    candidates = query.all()
    
    # Filter by skills if provided
    if skills:
        skill_list = [skill.strip().lower() for skill in skills.split(',')]
        filtered_candidates = []
        for candidate in candidates:
            candidate_skills = [skill.lower() for skill in candidate.get_skills_list()]
            if any(skill in candidate_skills for skill in skill_list):
                filtered_candidates.append(candidate)
        candidates = filtered_candidates
    
    return jsonify([candidate.to_dict() for candidate in candidates])

@candidate_bp.route('/candidates', methods=['POST'])
def create_candidate():
    """Create a new candidate profile"""
    data = request.json
    
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if candidate with this email already exists
    existing_candidate = Candidate.query.filter_by(email=data['email']).first()
    if existing_candidate:
        return jsonify({'error': 'Candidate with this email already exists'}), 409
    
    candidate = Candidate(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        linkedin_profile=data.get('linkedin_profile'),
        total_experience_years=data.get('total_experience_years'),
        education=data.get('education'),
        parsed_cv_text=data.get('parsed_cv_text'),
        cv_file_path=data.get('cv_file_path')
    )
    
    # Handle skills list
    if 'skills' in data and isinstance(data['skills'], list):
        candidate.set_skills_list(data['skills'])
    
    db.session.add(candidate)
    db.session.commit()
    return jsonify(candidate.to_dict()), 201

@candidate_bp.route('/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get a specific candidate by ID"""
    candidate = Candidate.query.get_or_404(candidate_id)
    return jsonify(candidate.to_dict())

@candidate_bp.route('/candidates/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    """Update an existing candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    data = request.json
    
    # Update fields if provided
    candidate.first_name = data.get('first_name', candidate.first_name)
    candidate.last_name = data.get('last_name', candidate.last_name)
    candidate.email = data.get('email', candidate.email)
    candidate.phone = data.get('phone', candidate.phone)
    candidate.linkedin_profile = data.get('linkedin_profile', candidate.linkedin_profile)
    candidate.total_experience_years = data.get('total_experience_years', candidate.total_experience_years)
    candidate.education = data.get('education', candidate.education)
    candidate.parsed_cv_text = data.get('parsed_cv_text', candidate.parsed_cv_text)
    candidate.cv_file_path = data.get('cv_file_path', candidate.cv_file_path)
    
    # Handle skills list update
    if 'skills' in data and isinstance(data['skills'], list):
        candidate.set_skills_list(data['skills'])
    
    db.session.commit()
    return jsonify(candidate.to_dict())

@candidate_bp.route('/candidates/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """Delete a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    db.session.delete(candidate)
    db.session.commit()
    return '', 204

@candidate_bp.route('/candidates/<int:candidate_id>/applications', methods=['GET'])
def get_candidate_applications(candidate_id):
    """Get all applications for a specific candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    applications = [app.to_dict_with_details() for app in candidate.applications]
    return jsonify(applications)

