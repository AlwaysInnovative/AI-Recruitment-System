from flask import Blueprint, jsonify, request
from src.models.application import Application, db
from src.models.communication import CommunicationLog
from src.models.agency import RecruitmentAgency
from src.services.communication import CommunicationService, DocumentGenerator
from src.services.ai_matcher import AIMatchingEngine
from datetime import datetime

communication_bp = Blueprint('communication', __name__)

# Initialize services
comm_service = CommunicationService()
doc_generator = DocumentGenerator()
ai_matcher = AIMatchingEngine()

@communication_bp.route('/communications/email', methods=['POST'])
def send_email():
    """Send email to candidate"""
    data = request.json
    
    required_fields = ['recipient', 'subject', 'body']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Send email
    result = comm_service.send_email(
        to_email=data['recipient'],
        subject=data['subject'],
        body=data['body']
    )
    
    # Log communication if application_id is provided
    if 'application_id' in data:
        log = CommunicationLog(
            application_id=data['application_id'],
            type='email',
            subject=data['subject'],
            body=data['body'],
            recipient=data['recipient'],
            status=result['status'],
            provider_response=result.get('provider_response')
        )
        db.session.add(log)
        db.session.commit()
    
    return jsonify(result)

@communication_bp.route('/communications/email/template', methods=['POST'])
def send_template_email():
    """Send templated email to candidate"""
    data = request.json
    
    required_fields = ['recipient', 'template_id', 'placeholders']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Send templated email
    result = comm_service.send_email(
        to_email=data['recipient'],
        subject='',  # Will be filled by template
        body='',     # Will be filled by template
        template_id=data['template_id'],
        placeholders=data['placeholders']
    )
    
    # Log communication if application_id is provided
    if 'application_id' in data:
        template = comm_service.get_email_template(data['template_id'])
        if template:
            subject = comm_service.render_template(template['subject'], data['placeholders'])
            body = comm_service.render_template(template['body'], data['placeholders'])
            
            log = CommunicationLog(
                application_id=data['application_id'],
                type='email',
                subject=subject,
                body=body,
                recipient=data['recipient'],
                status=result['status'],
                provider_response=result.get('provider_response')
            )
            db.session.add(log)
            db.session.commit()
    
    return jsonify(result)

@communication_bp.route('/communications/sms', methods=['POST'])
def send_sms():
    """Send SMS to candidate"""
    data = request.json
    
    required_fields = ['recipient', 'message']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Send SMS
    result = comm_service.send_sms(
        to_phone=data['recipient'],
        message=data['message']
    )
    
    # Log communication if application_id is provided
    if 'application_id' in data:
        log = CommunicationLog(
            application_id=data['application_id'],
            type='sms',
            body=data['message'],
            recipient=data['recipient'],
            status=result['status'],
            provider_response=result.get('provider_response')
        )
        db.session.add(log)
        db.session.commit()
    
    return jsonify(result)

@communication_bp.route('/communications/sms/template', methods=['POST'])
def send_template_sms():
    """Send templated SMS to candidate"""
    data = request.json
    
    required_fields = ['recipient', 'template_id', 'placeholders']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Send templated SMS
    result = comm_service.send_sms(
        to_phone=data['recipient'],
        message='',  # Will be filled by template
        template_id=data['template_id'],
        placeholders=data['placeholders']
    )
    
    # Log communication if application_id is provided
    if 'application_id' in data:
        template_message = comm_service.get_sms_template(data['template_id'])
        if template_message:
            message = comm_service.render_template(template_message, data['placeholders'])
            
            log = CommunicationLog(
                application_id=data['application_id'],
                type='sms',
                body=message,
                recipient=data['recipient'],
                status=result['status'],
                provider_response=result.get('provider_response')
            )
            db.session.add(log)
            db.session.commit()
    
    return jsonify(result)

@communication_bp.route('/communications/automated/application-received', methods=['POST'])
def send_application_received():
    """Send automated application received notification"""
    data = request.json
    
    if 'application_id' not in data:
        return jsonify({'error': 'Missing required field: application_id'}), 400
    
    application = Application.query.get_or_404(data['application_id'])
    
    # Prepare placeholders
    placeholders = {
        'candidate_name': f"{application.candidate.first_name} {application.candidate.last_name}",
        'job_title': application.job.title,
        'company_name': data.get('company_name', 'Our Company')
    }
    
    # Send email
    email_result = comm_service.send_email(
        to_email=application.candidate.email,
        subject='',
        body='',
        template_id='application_acknowledgment',
        placeholders=placeholders
    )
    
    # Send SMS if phone number is available
    sms_result = None
    if application.candidate.phone:
        sms_result = comm_service.send_sms(
            to_phone=application.candidate.phone,
            message='',
            template_id='application_confirmation',
            placeholders=placeholders
        )
    
    # Log communications
    template = comm_service.get_email_template('application_acknowledgment')
    if template:
        subject = comm_service.render_template(template['subject'], placeholders)
        body = comm_service.render_template(template['body'], placeholders)
        
        email_log = CommunicationLog(
            application_id=application.id,
            type='email',
            subject=subject,
            body=body,
            recipient=application.candidate.email,
            status=email_result['status'],
            provider_response=email_result.get('provider_response')
        )
        db.session.add(email_log)
    
    if sms_result and application.candidate.phone:
        sms_template = comm_service.get_sms_template('application_confirmation')
        if sms_template:
            message = comm_service.render_template(sms_template, placeholders)
            
            sms_log = CommunicationLog(
                application_id=application.id,
                type='sms',
                body=message,
                recipient=application.candidate.phone,
                status=sms_result['status'],
                provider_response=sms_result.get('provider_response')
            )
            db.session.add(sms_log)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Application received notifications sent',
        'email_result': email_result,
        'sms_result': sms_result
    })

@communication_bp.route('/communications/automated/information-request', methods=['POST'])
def send_information_request():
    """Send automated information request when matching threshold is met"""
    data = request.json
    
    if 'application_id' not in data:
        return jsonify({'error': 'Missing required field: application_id'}), 400
    
    application = Application.query.get_or_404(data['application_id'])
    
    # Check if matching score meets threshold
    threshold = data.get('threshold', 0.6)
    if not application.matching_score or application.matching_score < threshold:
        return jsonify({'error': f'Matching score {application.matching_score} does not meet threshold {threshold}'}), 400
    
    # Prepare placeholders
    placeholders = {
        'candidate_name': f"{application.candidate.first_name} {application.candidate.last_name}",
        'job_title': application.job.title,
        'company_name': data.get('company_name', 'Our Company'),
        'matching_score': int(application.matching_score * 100),
        'hiring_manager_name': data.get('hiring_manager_name', 'Hiring Manager'),
        'job_location': application.job.location or 'TBD'
    }
    
    # Send email
    result = comm_service.send_email(
        to_email=application.candidate.email,
        subject='',
        body='',
        template_id='information_request',
        placeholders=placeholders
    )
    
    # Log communication
    template = comm_service.get_email_template('information_request')
    if template:
        subject = comm_service.render_template(template['subject'], placeholders)
        body = comm_service.render_template(template['body'], placeholders)
        
        log = CommunicationLog(
            application_id=application.id,
            type='email',
            subject=subject,
            body=body,
            recipient=application.candidate.email,
            status=result['status'],
            provider_response=result.get('provider_response')
        )
        db.session.add(log)
        db.session.commit()
    
    return jsonify({
        'message': 'Information request sent',
        'result': result,
        'matching_score': application.matching_score
    })

@communication_bp.route('/documents/candidate-summary', methods=['POST'])
def generate_candidate_summary():
    """Generate candidate summary for hiring manager"""
    data = request.json
    
    if 'application_id' not in data:
        return jsonify({'error': 'Missing required field: application_id'}), 400
    
    application = Application.query.get_or_404(data['application_id'])
    
    # Get candidate and job data
    candidate_data = application.candidate.to_dict()
    job_data = application.job.to_dict()
    
    # Get or calculate match details
    if application.matching_score:
        # Use existing score and calculate breakdown
        match_details = ai_matcher.get_match_details(candidate_data, job_data)
    else:
        # Calculate new matching score
        match_details = ai_matcher.get_match_details(candidate_data, job_data)
        application.matching_score = match_details['overall_score']
        db.session.commit()
    
    # Generate summary document
    summary = doc_generator.generate_candidate_summary(candidate_data, job_data, match_details)
    
    return jsonify({
        'summary': summary,
        'candidate_id': application.candidate_id,
        'job_id': application.job_id,
        'application_id': application.id,
        'match_details': match_details
    })

@communication_bp.route('/documents/right-to-representation', methods=['POST'])
def generate_right_to_representation():
    """Generate right to representation agreement"""
    data = request.json
    
    required_fields = ['application_id', 'agency_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    application = Application.query.get_or_404(data['application_id'])
    agency = RecruitmentAgency.query.get_or_404(data['agency_id'])
    
    # Get data
    candidate_data = application.candidate.to_dict()
    job_data = application.job.to_dict()
    agency_data = agency.to_dict()
    
    # Generate agreement document
    agreement = doc_generator.generate_right_to_representation_agreement(
        candidate_data, agency_data, job_data
    )
    
    return jsonify({
        'agreement': agreement,
        'candidate_id': application.candidate_id,
        'job_id': application.job_id,
        'application_id': application.id,
        'agency_id': agency.id
    })

@communication_bp.route('/communications/templates/email', methods=['GET'])
def list_email_templates():
    """List available email templates"""
    templates = comm_service.list_email_templates()
    template_details = {}
    
    for template_id in templates:
        template_details[template_id] = comm_service.get_email_template(template_id)
    
    return jsonify({
        'templates': template_details
    })

@communication_bp.route('/communications/templates/sms', methods=['GET'])
def list_sms_templates():
    """List available SMS templates"""
    templates = comm_service.list_sms_templates()
    template_details = {}
    
    for template_id in templates:
        template_details[template_id] = comm_service.get_sms_template(template_id)
    
    return jsonify({
        'templates': template_details
    })

@communication_bp.route('/communications/logs/<int:application_id>', methods=['GET'])
def get_communication_logs(application_id):
    """Get communication logs for an application"""
    application = Application.query.get_or_404(application_id)
    
    logs = [log.to_dict() for log in application.communications]
    
    return jsonify({
        'application_id': application_id,
        'logs': logs
    })

