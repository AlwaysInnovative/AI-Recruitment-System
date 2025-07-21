import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from datetime import datetime
import os
import re

class CommunicationService:
    """Service for handling automated email and SMS communications"""
    
    def __init__(self):
        # Email configuration (would be loaded from environment variables in production)
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', 'noreply@company.com')
        self.smtp_password = os.getenv('SMTP_PASSWORD', 'password')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@company.com')
        
        # SMS configuration (would integrate with Twilio or similar)
        self.sms_api_key = os.getenv('SMS_API_KEY', 'dummy_key')
        self.sms_from_number = os.getenv('SMS_FROM_NUMBER', '+1234567890')
        
        # Email templates
        self.email_templates = {
            'application_acknowledgment': {
                'subject': 'Application Received - {{job_title}}',
                'body': '''
Dear {{candidate_name}},

Thank you for your interest in the {{job_title}} position at {{company_name}}.

We have received your application and our team is currently reviewing it. Our AI-powered system has analyzed your profile and we're excited to learn more about your background.

We will be in touch within the next few business days with next steps.

Best regards,
{{company_name}} Recruitment Team

---
This is an automated message. Please do not reply to this email.
'''
            },
            'information_request': {
                'subject': 'Additional Information Needed - {{job_title}}',
                'body': '''
Dear {{candidate_name}},

Thank you for your application for the {{job_title}} position at {{company_name}}.

Our initial review shows that you may be a good fit for this role (matching score: {{matching_score}}%). We would like to gather some additional information to better understand your background and expectations.

Please provide the following information:

1. Your salary expectations for this role
2. Your preferred work arrangement (remote, hybrid, on-site)
3. Your availability to start
4. Any specific requirements or preferences you have

Please reply to this email with the requested information at your earliest convenience.

We look forward to hearing from you!

Best regards,
{{hiring_manager_name}}
{{company_name}}

---
Position: {{job_title}}
Location: {{job_location}}
'''
            },
            'right_to_representation': {
                'subject': 'Right to Representation Agreement - {{job_title}}',
                'body': '''
Dear {{candidate_name}},

We are pleased to inform you that you have progressed in our selection process for the {{job_title}} position.

As part of our process, we need you to review and sign the attached Right to Representation agreement. This agreement allows us to represent you in discussions with our client company and ensures proper handling of your application.

Key points of the agreement:
- We will represent your interests throughout the recruitment process
- All communications with the client will go through our team
- Your personal information will be handled confidentially
- Commission arrangements are between us and the client company

Please review the agreement carefully and reply with your electronic signature if you agree to the terms.

If you have any questions about the agreement, please don't hesitate to contact us.

Best regards,
{{agency_contact_person}}
{{agency_name}}

Phone: {{agency_phone}}
Email: {{agency_email}}
'''
            },
            'interview_invitation': {
                'subject': 'Interview Invitation - {{job_title}}',
                'body': '''
Dear {{candidate_name}},

Congratulations! We would like to invite you for an interview for the {{job_title}} position at {{company_name}}.

Interview Details:
- Date: {{interview_date}}
- Time: {{interview_time}}
- Format: {{interview_format}}
- Duration: Approximately {{interview_duration}}

{{interview_instructions}}

Please confirm your availability by replying to this email. If the proposed time doesn't work for you, please suggest alternative times.

We look forward to speaking with you!

Best regards,
{{hiring_manager_name}}
{{company_name}}
'''
            },
            'hiring_manager_summary': {
                'subject': 'Candidate Summary - {{candidate_name}} for {{job_title}}',
                'body': '''
Dear {{hiring_manager_name}},

Please find below a summary of candidate {{candidate_name}} who has applied for the {{job_title}} position.

CANDIDATE OVERVIEW:
- Name: {{candidate_name}}
- Email: {{candidate_email}}
- Phone: {{candidate_phone}}
- LinkedIn: {{candidate_linkedin}}
- Experience: {{candidate_experience}} years

AI MATCHING ANALYSIS:
- Overall Match Score: {{matching_score}}%
- Skills Match: {{skills_match_score}}%
- Experience Match: {{experience_match_score}}%
- Education Match: {{education_match_score}}%

KEY SKILLS:
{{candidate_skills}}

EXPERIENCE HIGHLIGHTS:
{{experience_highlights}}

EDUCATION:
{{candidate_education}}

RECOMMENDATION:
{{recommendation}}

The candidate has completed our initial screening and {{right_to_representation_status}}.

To proceed with this candidate, please log into the recruitment dashboard or reply to this email.

Best regards,
Recruitment AI System
'''
            }
        }
        
        # SMS templates
        self.sms_templates = {
            'application_confirmation': 'Hi {{candidate_name}}, your application for {{job_title}} at {{company_name}} has been received. Check your email for details.',
            'interview_reminder': 'Reminder: You have an interview for {{job_title}} at {{company_name}} tomorrow at {{interview_time}}. Good luck!',
            'status_update': 'Update on your {{job_title}} application: {{status_message}}. Check your email for details.'
        }
    
    def render_template(self, template: str, placeholders: Dict[str, str]) -> str:
        """Render template with placeholders"""
        for key, value in placeholders.items():
            template = template.replace(f'{{{{{key}}}}}', str(value))
        return template
    
    def send_email(self, to_email: str, subject: str, body: str, template_id: str = None, placeholders: Dict[str, str] = None) -> Dict[str, str]:
        """Send email (simulated for demo purposes)"""
        try:
            # In a real implementation, this would use SMTP
            # For demo purposes, we'll just log the email
            
            if template_id and placeholders:
                if template_id in self.email_templates:
                    template = self.email_templates[template_id]
                    subject = self.render_template(template['subject'], placeholders)
                    body = self.render_template(template['body'], placeholders)
            
            # Simulate email sending
            print(f"[EMAIL SENT]")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body[:100]}...")
            
            return {
                'status': 'sent',
                'message': 'Email sent successfully',
                'provider_response': f'Simulated email to {to_email}'
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'message': f'Failed to send email: {str(e)}',
                'provider_response': str(e)
            }
    
    def send_sms(self, to_phone: str, message: str, template_id: str = None, placeholders: Dict[str, str] = None) -> Dict[str, str]:
        """Send SMS (simulated for demo purposes)"""
        try:
            if template_id and placeholders:
                if template_id in self.sms_templates:
                    message = self.render_template(self.sms_templates[template_id], placeholders)
            
            # Simulate SMS sending
            print(f"[SMS SENT]")
            print(f"To: {to_phone}")
            print(f"Message: {message}")
            
            return {
                'status': 'sent',
                'message': 'SMS sent successfully',
                'provider_response': f'Simulated SMS to {to_phone}'
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'message': f'Failed to send SMS: {str(e)}',
                'provider_response': str(e)
            }
    
    def get_email_template(self, template_id: str) -> Optional[Dict[str, str]]:
        """Get email template by ID"""
        return self.email_templates.get(template_id)
    
    def get_sms_template(self, template_id: str) -> Optional[str]:
        """Get SMS template by ID"""
        return self.sms_templates.get(template_id)
    
    def list_email_templates(self) -> List[str]:
        """List available email template IDs"""
        return list(self.email_templates.keys())
    
    def list_sms_templates(self) -> List[str]:
        """List available SMS template IDs"""
        return list(self.sms_templates.keys())

class DocumentGenerator:
    """Service for generating recruitment-related documents"""
    
    def __init__(self):
        pass
    
    def generate_candidate_summary(self, candidate_data: Dict, job_data: Dict, match_details: Dict) -> str:
        """Generate a comprehensive candidate summary for hiring managers"""
        
        # Extract data
        candidate_name = f"{candidate_data.get('first_name', '')} {candidate_data.get('last_name', '')}"
        skills = candidate_data.get('skills', [])
        experience = candidate_data.get('total_experience_years', 'Not specified')
        education = candidate_data.get('education', 'Not specified')
        
        # Format skills
        skills_text = ', '.join(skills) if skills else 'Not specified'
        
        # Generate recommendation based on matching score
        overall_score = match_details.get('overall_score', 0)
        if overall_score >= 0.8:
            recommendation = "HIGHLY RECOMMENDED - Excellent match for this position"
        elif overall_score >= 0.6:
            recommendation = "RECOMMENDED - Good match with some areas to explore"
        elif overall_score >= 0.4:
            recommendation = "CONSIDER - Moderate match, may need additional evaluation"
        else:
            recommendation = "NOT RECOMMENDED - Poor match for this position"
        
        # Generate experience highlights
        experience_highlights = "Based on CV analysis:\n"
        if candidate_data.get('parsed_cv_text'):
            cv_text = candidate_data['parsed_cv_text']
            # Extract key experience points (simplified)
            lines = cv_text.split('\n')
            experience_lines = [line.strip() for line in lines if 
                              any(keyword in line.lower() for keyword in ['experience', 'worked', 'developed', 'led', 'managed', 'built'])]
            experience_highlights += '\n'.join(experience_lines[:5])
        else:
            experience_highlights += "No detailed experience information available"
        
        summary = f"""
CANDIDATE PROFILE SUMMARY
========================

Candidate: {candidate_name}
Position: {job_data.get('title', 'N/A')}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

CONTACT INFORMATION:
- Email: {candidate_data.get('email', 'Not provided')}
- Phone: {candidate_data.get('phone', 'Not provided')}
- LinkedIn: {candidate_data.get('linkedin_profile', 'Not provided')}

EXPERIENCE:
- Total Years: {experience} years
- Level: {'Senior' if isinstance(experience, (int, float)) and experience >= 7 else 'Mid-level' if isinstance(experience, (int, float)) and experience >= 3 else 'Junior'}

EDUCATION:
{education}

TECHNICAL SKILLS:
{skills_text}

AI MATCHING ANALYSIS:
- Overall Match Score: {overall_score * 100:.1f}%
- Skills Compatibility: {match_details.get('breakdown', {}).get('skills_match', 0) * 100:.1f}%
- Experience Alignment: {match_details.get('breakdown', {}).get('experience_match', 0) * 100:.1f}%
- Education Match: {match_details.get('breakdown', {}).get('education_match', 0) * 100:.1f}%
- Keyword Relevance: {match_details.get('breakdown', {}).get('keyword_match', 0) * 100:.1f}%

EXPERIENCE HIGHLIGHTS:
{experience_highlights}

RECOMMENDATION:
{recommendation}

NEXT STEPS:
{'✓ Proceed to interview stage' if overall_score >= 0.6 else '? Requires additional screening' if overall_score >= 0.4 else '✗ Consider other candidates'}

---
Generated by AI Recruitment System
"""
        return summary
    
    def generate_right_to_representation_agreement(self, candidate_data: Dict, agency_data: Dict, job_data: Dict) -> str:
        """Generate right to representation agreement document"""
        
        candidate_name = f"{candidate_data.get('first_name', '')} {candidate_data.get('last_name', '')}"
        agency_name = agency_data.get('name', 'Recruitment Agency')
        job_title = job_data.get('title', 'Position')
        
        agreement = f"""
RIGHT TO REPRESENTATION AGREEMENT
=================================

Date: {datetime.now().strftime('%Y-%m-%d')}

PARTIES:
Candidate: {candidate_name}
Email: {candidate_data.get('email', '')}

Recruitment Agency: {agency_name}
Contact: {agency_data.get('contact_person', '')}
Email: {agency_data.get('email', '')}
Phone: {agency_data.get('phone', '')}

POSITION:
Title: {job_title}
Company: {job_data.get('company_name', 'Client Company')}
Location: {job_data.get('location', 'TBD')}

AGREEMENT TERMS:

1. REPRESENTATION AUTHORIZATION
   The Candidate hereby authorizes {agency_name} to represent them in all matters 
   related to the above-mentioned position, including but not limited to:
   - Submitting candidate profile to the client company
   - Negotiating terms and conditions of employment
   - Facilitating communication between candidate and client

2. EXCLUSIVITY
   This agreement grants {agency_name} exclusive rights to represent the Candidate 
   for this specific position for a period of 90 days from the date of this agreement.

3. CONFIDENTIALITY
   Both parties agree to maintain confidentiality of all information shared during 
   the recruitment process.

4. COMMISSION
   The Candidate acknowledges that {agency_name} will receive a commission from the 
   client company upon successful placement. This commission does not affect the 
   candidate's salary or benefits.

5. TERMINATION
   Either party may terminate this agreement with 48 hours written notice.

6. CANDIDATE OBLIGATIONS
   The Candidate agrees to:
   - Provide accurate and complete information
   - Respond promptly to communications
   - Attend scheduled interviews and meetings
   - Notify the agency of any direct contact from the client company

7. AGENCY OBLIGATIONS
   {agency_name} agrees to:
   - Represent the candidate's interests professionally
   - Provide regular updates on the recruitment process
   - Maintain confidentiality of candidate information
   - Act in good faith throughout the process

By signing below, both parties acknowledge they have read, understood, and agree 
to be bound by the terms of this agreement.

CANDIDATE SIGNATURE:
Name: {candidate_name}
Date: ________________
Signature: ________________

AGENCY REPRESENTATIVE:
Name: {agency_data.get('contact_person', '')}
Title: Recruitment Consultant
Date: {datetime.now().strftime('%Y-%m-%d')}
Signature: [Digital Signature]

---
{agency_name}
{agency_data.get('email', '')}
{agency_data.get('phone', '')}
"""
        return agreement

