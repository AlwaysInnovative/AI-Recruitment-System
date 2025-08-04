from flask import Blueprint, jsonify
from src.models.application import Application
from src.models.job import Job
from src.models.candidate import Candidate
from src.models.agency import RecruitmentAgency, RecruitmentAgencyCommission
from datetime import datetime, timedelta

overview_bp = Blueprint('overview', __name__)

@overview_bp.route('/stats', methods=['GET'])
def get_overview_stats():
    """Endpoint for dashboard summary statistics"""
    now = datetime.utcnow()
    time_ranges = {
        'week': now - timedelta(days=7),
        'month': now - timedelta(days=30),
        'quarter': now - timedelta(days=90)
    }

    stats = {
        'jobs': {
            'total': Job.query.count(),
            'active': Job.query.filter_by(status='open').count(),
            'new_last_week': Job.query.filter(
                Job.created_at >= time_ranges['week']
            ).count()
        },
        'candidates': {
            'total': Candidate.query.count(),
            'new_last_week': Candidate.query.filter(
                Candidate.created_at >= time_ranges['week']
            ).count(),
            'active': Application.query.distinct(
                Application.candidate_id
            ).count()
        },
        'applications': {
            'total': Application.query.count(),
            'by_status': {
                status: Application.query.filter_by(
                    status=status
                ).count() 
                for status in ['applied', 'reviewed', 'interviewed', 'hired', 'rejected']
            },
            'hires': {
                'week': Application.query.filter(
                    Application.status == 'hired',
                    Application.updated_at >= time_ranges['week']
                ).count(),
                'month': Application.query.filter(
                    Application.status == 'hired',
                    Application.updated_at >= time_ranges['month']
                ).count()
            }
        },
        'financials': {
            'pending_commissions': RecruitmentAgencyCommission.query.filter_by(
                status='pending'
            ).count(),
            'total_payouts': sum(
                c.amount for c in RecruitmentAgencyCommission.query.filter_by(
                    status='paid'
                ).all()
            ) or 0
        }
    }
    return jsonify(stats)

@overview_bp.route('/activity', methods=['GET'])
def get_recent_activity():
    """Endpoint for recent system activity"""
    activities = []
    
    # Recent applications
    recent_apps = Application.query.order_by(
        Application.updated_at.desc()
    ).limit(5).all()
    
    for app in recent_apps:
        activities.append({
            'type': 'application',
            'id': app.id,
            'candidate': app.candidate.name,
            'job': app.job.title,
            'status': app.status,
            'time': app.updated_at.isoformat()
        })
    
    # Recent commissions
    recent_commissions = RecruitmentAgencyCommission.query.order_by(
        RecruitmentAgencyCommission.updated_at.desc()
    ).limit(3).all()
    
    for comm in recent_commissions:
        activities.append({
            'type': 'commission',
            'id': comm.id,
            'amount': comm.amount,
            'agency': comm.agency.name,
            'status': comm.status,
            'time': comm.updated_at.isoformat()
        })
    
    return jsonify({'activities': activities})
