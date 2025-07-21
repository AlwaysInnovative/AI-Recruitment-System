from flask import Blueprint, jsonify, request
from src.models.application import Application, db
from src.models.job import Job
from src.models.candidate import Candidate
from src.services.ai_matcher import AIMatchingEngine
from src.services.cv_processor import CVProcessor

matching_bp = Blueprint('matching', __name__)

# Initialize services
ai_matcher = AIMatchingEngine()
cv_processor = CVProcessor()

@matching_bp.route('/match', methods=['POST'])
def calculate_match():
    """Calculate matching score for a specific application"""
    data = request.json
    
    if 'application_id' not in data:
        return jsonify({'error': 'Missing required field: application_id'}), 400
    
    application = Application.query.get_or_404(data['application_id'])
    
    # Get candidate and job data
    candidate_data = application.candidate.to_dict()
    job_data = application.job.to_dict()
    
    # Calculate matching score
    matching_score = ai_matcher.calculate_matching_score(candidate_data, job_data)
    
    # Update application with matching score
    application.matching_score = matching_score
    db.session.commit()
    
    return jsonify({
        'application_id': application.id,
        'matching_score': matching_score,
        'candidate_id': application.candidate_id,
        'job_id': application.job_id
    })

@matching_bp.route('/match/detailed', methods=['POST'])
def calculate_detailed_match():
    """Calculate detailed matching score breakdown for a specific application"""
    data = request.json
    
    if 'application_id' not in data:
        return jsonify({'error': 'Missing required field: application_id'}), 400
    
    application = Application.query.get_or_404(data['application_id'])
    
    # Get candidate and job data
    candidate_data = application.candidate.to_dict()
    job_data = application.job.to_dict()
    
    # Calculate detailed matching scores
    match_details = ai_matcher.get_match_details(candidate_data, job_data)
    
    # Update application with matching score
    application.matching_score = match_details['overall_score']
    db.session.commit()
    
    return jsonify({
        'application_id': application.id,
        'candidate_id': application.candidate_id,
        'job_id': application.job_id,
        'match_details': match_details
    })

@matching_bp.route('/match/batch', methods=['POST'])
def calculate_batch_match():
    """Calculate matching scores for multiple applications"""
    data = request.json
    
    if 'application_ids' not in data or not isinstance(data['application_ids'], list):
        return jsonify({'error': 'Missing or invalid field: application_ids (must be a list)'}), 400
    
    results = []
    
    for app_id in data['application_ids']:
        try:
            application = Application.query.get(app_id)
            if not application:
                results.append({
                    'application_id': app_id,
                    'error': 'Application not found'
                })
                continue
            
            # Get candidate and job data
            candidate_data = application.candidate.to_dict()
            job_data = application.job.to_dict()
            
            # Calculate matching score
            matching_score = ai_matcher.calculate_matching_score(candidate_data, job_data)
            
            # Update application with matching score
            application.matching_score = matching_score
            
            results.append({
                'application_id': application.id,
                'matching_score': matching_score,
                'candidate_id': application.candidate_id,
                'job_id': application.job_id
            })
            
        except Exception as e:
            results.append({
                'application_id': app_id,
                'error': str(e)
            })
    
    # Commit all updates
    db.session.commit()
    
    return jsonify({'results': results})

@matching_bp.route('/match/job/<int:job_id>', methods=['POST'])
def match_candidates_to_job(job_id):
    """Find and rank all candidates for a specific job"""
    job = Job.query.get_or_404(job_id)
    
    # Get all candidates
    candidates = Candidate.query.all()
    
    if not candidates:
        return jsonify({'message': 'No candidates found', 'matches': []})
    
    job_data = job.to_dict()
    matches = []
    
    for candidate in candidates:
        candidate_data = candidate.to_dict()
        
        # Calculate matching score
        matching_score = ai_matcher.calculate_matching_score(candidate_data, job_data)
        
        matches.append({
            'candidate_id': candidate.id,
            'candidate_name': f"{candidate.first_name} {candidate.last_name}",
            'candidate_email': candidate.email,
            'matching_score': matching_score,
            'candidate_skills': candidate.get_skills_list(),
            'candidate_experience': candidate.total_experience_years
        })
    
    # Sort by matching score (highest first)
    matches.sort(key=lambda x: x['matching_score'], reverse=True)
    
    # Get threshold from request or use default
    threshold = request.args.get('threshold', 0.6, type=float)
    qualified_matches = [match for match in matches if match['matching_score'] >= threshold]
    
    return jsonify({
        'job_id': job_id,
        'job_title': job.title,
        'total_candidates': len(candidates),
        'qualified_candidates': len(qualified_matches),
        'threshold': threshold,
        'matches': qualified_matches
    })

@matching_bp.route('/process-cv', methods=['POST'])
def process_cv_text():
    """Process CV text and extract structured information"""
    data = request.json
    
    if 'cv_text' not in data:
        return jsonify({'error': 'Missing required field: cv_text'}), 400
    
    cv_text = data['cv_text']
    
    # Process CV and extract information
    processed_data = cv_processor.process_cv(cv_text)
    
    return jsonify({
        'processed_data': processed_data,
        'message': 'CV processed successfully'
    })

@matching_bp.route('/process-cv-and-create-candidate', methods=['POST'])
def process_cv_and_create_candidate():
    """Process CV text and create a new candidate profile"""
    data = request.json
    
    if 'cv_text' not in data:
        return jsonify({'error': 'Missing required field: cv_text'}), 400
    
    cv_text = data['cv_text']
    
    # Process CV and extract information
    processed_data = cv_processor.process_cv(cv_text)
    
    # Check if required fields are present
    if not processed_data.get('email'):
        return jsonify({'error': 'Could not extract email from CV'}), 400
    
    if not processed_data.get('first_name') or not processed_data.get('last_name'):
        return jsonify({'error': 'Could not extract name from CV'}), 400
    
    # Check if candidate already exists
    existing_candidate = Candidate.query.filter_by(email=processed_data['email']).first()
    if existing_candidate:
        return jsonify({'error': 'Candidate with this email already exists', 'candidate_id': existing_candidate.id}), 409
    
    # Create new candidate
    candidate = Candidate(
        first_name=processed_data['first_name'],
        last_name=processed_data['last_name'],
        email=processed_data['email'],
        phone=processed_data.get('phone'),
        linkedin_profile=processed_data.get('linkedin_profile'),
        total_experience_years=processed_data.get('total_experience_years'),
        education=processed_data.get('education'),
        parsed_cv_text=processed_data.get('parsed_cv_text'),
        cv_file_path=data.get('cv_file_path')
    )
    
    # Set skills
    if processed_data.get('skills'):
        candidate.set_skills_list(processed_data['skills'])
    
    db.session.add(candidate)
    db.session.commit()
    
    return jsonify({
        'message': 'Candidate created successfully',
        'candidate': candidate.to_dict(),
        'processed_data': processed_data
    }), 201

