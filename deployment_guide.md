# AI-Powered Recruitment System - Deployment Guide

## System Overview

This comprehensive AI-powered recruitment system automates the entire hiring process from CV analysis to candidate communication and commission management.

## Architecture

### Backend (Flask API)
- **Location**: `/home/ubuntu/recruitment_backend/`
- **Port**: 5001
- **Database**: SQLite (development) / PostgreSQL (production)
- **Key Features**:
  - CV processing and AI matching
  - Automated communications (email/SMS)
  - Document generation
  - Commission management
  - RESTful API endpoints

### Frontend (React Dashboard)
- **Location**: `/home/ubuntu/recruitment-dashboard/`
- **Port**: 5173 (development) / 80 (production)
- **Framework**: React with Vite
- **UI Library**: shadcn/ui with Tailwind CSS
- **Key Features**:
  - Interactive dashboard
  - Job and candidate management
  - Application review with AI scores
  - Communication management

## Deployment Instructions

### Prerequisites
- Python 3.11+
- Node.js 20+
- pnpm package manager

### Backend Deployment

1. **Navigate to backend directory**:
   ```bash
   cd /home/ubuntu/recruitment_backend
   ```

2. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (production):
   ```bash
   export FLASK_ENV=production
   export DATABASE_URL=postgresql://user:password@host:port/dbname
   export SMTP_SERVER=smtp.gmail.com
   export SMTP_USERNAME=your-email@gmail.com
   export SMTP_PASSWORD=your-app-password
   export SMS_API_KEY=your-twilio-api-key
   ```

5. **Initialize database**:
   ```bash
   python -c "from src.models.user import db; db.create_all()"
   ```

6. **Start the application**:
   ```bash
   python src/main.py
   ```

### Frontend Deployment

1. **Navigate to frontend directory**:
   ```bash
   cd /home/ubuntu/recruitment-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pnpm install
   ```

3. **Build for production**:
   ```bash
   pnpm run build
   ```

4. **Serve the application**:
   ```bash
   pnpm run preview
   ```

### Production Deployment Options

#### Option 1: Using Manus Deployment Services

**Backend Deployment**:
```bash
# Deploy Flask backend
manus-deploy-backend recruitment_backend flask
```

**Frontend Deployment**:
```bash
# Build and deploy React frontend
cd recruitment-dashboard
pnpm run build
manus-deploy-frontend dist static
```

#### Option 2: Traditional Server Deployment

**Backend (using Gunicorn)**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 src.main:app
```

**Frontend (using Nginx)**:
```bash
# Build the application
pnpm run build

# Copy to web server directory
sudo cp -r dist/* /var/www/html/

# Configure Nginx to serve the files
```

## API Endpoints

### Core Endpoints
- `GET /api/jobs` - List all jobs
- `POST /api/jobs` - Create new job
- `GET /api/candidates` - List all candidates
- `POST /api/candidates` - Create new candidate
- `GET /api/applications` - List all applications
- `POST /api/applications` - Create new application

### AI Matching
- `POST /api/process-cv` - Process CV text and extract information
- `POST /api/match` - Calculate AI matching score for application
- `POST /api/match/batch` - Batch matching for multiple candidates

### Communications
- `POST /api/communications/email` - Send email
- `POST /api/communications/sms` - Send SMS
- `POST /api/communications/automated/application-received` - Automated notification
- `POST /api/communications/automated/information-request` - Request candidate info

### Document Generation
- `POST /api/documents/candidate-summary` - Generate candidate summary
- `POST /api/documents/right-to-representation` - Generate agreement

### Commission Management
- `GET /api/commissions` - List commissions
- `POST /api/commissions` - Create commission record

## Configuration

### Environment Variables

**Backend**:
```bash
FLASK_ENV=production
DATABASE_URL=sqlite:///app.db
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-password
SMS_API_KEY=your-sms-api-key
```

**Frontend**:
```bash
VITE_API_BASE_URL=http://localhost:5001/api
```

## Database Schema

### Core Tables
- **users** - Hiring managers and system users
- **jobs** - Job postings with requirements
- **candidates** - Candidate profiles and CVs
- **applications** - Job applications with AI scores
- **recruitment_agencies** - Agency information
- **commissions** - Commission tracking
- **communication_logs** - Email/SMS history

## Security Considerations

1. **Authentication**: Implement JWT-based authentication
2. **Data Protection**: Encrypt sensitive candidate data
3. **API Security**: Rate limiting and input validation
4. **CORS**: Configure appropriate CORS policies
5. **Database**: Use parameterized queries to prevent SQL injection

## Monitoring and Maintenance

### Health Checks
- Backend: `GET /api/health`
- Frontend: Check if main page loads
- Database: Monitor connection pool and query performance

### Logging
- Application logs: `/home/ubuntu/recruitment_backend/flask.log`
- Error tracking: Implement Sentry or similar
- Performance monitoring: Monitor API response times

### Backup Strategy
- Database: Regular automated backups
- File storage: Backup uploaded CVs and documents
- Configuration: Version control for deployment configs

## Scaling Considerations

### Horizontal Scaling
- Load balancer for multiple backend instances
- CDN for frontend static assets
- Database read replicas for improved performance

### Performance Optimization
- Redis for caching frequently accessed data
- Background job processing for AI matching
- Database indexing for search operations

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Check database permissions
   - Verify connection string
   - Ensure database server is running

2. **API Timeout Issues**:
   - Increase timeout settings
   - Optimize database queries
   - Implement caching

3. **Frontend Build Errors**:
   - Clear node_modules and reinstall
   - Check for version conflicts
   - Verify environment variables

### Support Contacts
- Technical Support: [Your contact information]
- Documentation: [Link to detailed docs]
- Issue Tracking: [GitHub/GitLab repository]

## License and Compliance

- Ensure GDPR compliance for candidate data
- Implement data retention policies
- Regular security audits
- Compliance with employment laws

---

**Last Updated**: July 16, 2025
**Version**: 1.0.0

