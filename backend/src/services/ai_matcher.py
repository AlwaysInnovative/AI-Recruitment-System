import re
import math
from typing import Dict, List, Tuple, Optional
from collections import Counter
import json

class AIMatchingEngine:
    """AI-powered matching engine for scoring CV-to-job compatibility"""
    
    def __init__(self):
        # Weights for different matching criteria
        self.weights = {
            'skills_match': 0.4,
            'experience_match': 0.25,
            'education_match': 0.15,
            'keyword_match': 0.2
        }
        
        # Experience level mappings
        self.experience_levels = {
            'entry': (0, 2),
            'junior': (1, 3),
            'mid': (3, 7),
            'senior': (7, 12),
            'lead': (10, float('inf')),
            'principal': (12, float('inf'))
        }
    
    def preprocess_text(self, text: str) -> List[str]:
        """Preprocess text by cleaning and tokenizing"""
        # Handle None or empty text
        if not text:
            return []
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        return [word for word in words if word not in stop_words and len(word) > 2]
    
    def calculate_skills_match(self, candidate_skills: List[str], job_requirements: str) -> float:
        """Calculate skills matching score"""
        if not candidate_skills:
            return 0.0
        
        job_words = self.preprocess_text(job_requirements)
        job_skills_lower = [skill.lower() for skill in job_words]
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        
        # Count matching skills
        matches = 0
        total_job_skills = 0
        
        # Extract technical skills from job requirements
        technical_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'django', 'flask',
            'spring', 'node.js', 'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'docker',
            'kubernetes', 'git', 'machine learning', 'data science', 'ai', 'sql', 'html', 'css'
        ]
        
        for keyword in technical_keywords:
            if keyword in job_skills_lower:
                total_job_skills += 1
                if any(keyword in candidate_skill for candidate_skill in candidate_skills_lower):
                    matches += 1
        
        # Also check for direct skill matches
        for candidate_skill in candidate_skills_lower:
            if candidate_skill in job_skills_lower:
                matches += 1
                total_job_skills += 1
        
        if total_job_skills == 0:
            return 0.5  # Neutral score if no technical skills identified
        
        return min(matches / total_job_skills, 1.0)
    
    def calculate_experience_match(self, candidate_experience: Optional[float], job_requirements: str) -> float:
        """Calculate experience matching score"""
        if candidate_experience is None:
            return 0.5  # Neutral score if experience not specified
        
        # Extract experience requirements from job description
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\+?\s*years?\s*experience',
            r'minimum\s*(\d+)\s*years?',
            r'at\s*least\s*(\d+)\s*years?',
            r'(\d+)\+?\s*yrs?\s*experience'
        ]
        
        required_experience = None
        for pattern in experience_patterns:
            match = re.search(pattern, job_requirements, re.IGNORECASE)
            if match:
                required_experience = float(match.group(1))
                break
        
        # Check for experience level keywords
        job_lower = job_requirements.lower()
        if required_experience is None:
            if any(level in job_lower for level in ['entry', 'junior', 'graduate']):
                required_experience = 1.0
            elif any(level in job_lower for level in ['mid', 'intermediate']):
                required_experience = 4.0
            elif any(level in job_lower for level in ['senior', 'lead']):
                required_experience = 8.0
            elif any(level in job_lower for level in ['principal', 'architect']):
                required_experience = 12.0
            else:
                return 0.7  # Default good score if no experience requirement found
        
        # Calculate score based on how well candidate experience matches requirement
        if candidate_experience >= required_experience:
            # Bonus for having more experience, but diminishing returns
            excess = candidate_experience - required_experience
            bonus = min(excess / required_experience * 0.2, 0.3)
            return min(1.0 + bonus, 1.0)
        else:
            # Penalty for having less experience
            deficit = required_experience - candidate_experience
            penalty = deficit / required_experience
            return max(1.0 - penalty, 0.0)
    
    def calculate_education_match(self, candidate_education: Optional[str], job_requirements: str) -> float:
        """Calculate education matching score"""
        if not candidate_education:
            return 0.5  # Neutral score if education not specified
        
        candidate_edu_lower = candidate_education.lower()
        job_lower = job_requirements.lower()
        
        # Education level hierarchy
        education_levels = {
            'phd': 5, 'doctorate': 5, 'ph.d.': 5,
            'master': 4, 'mba': 4, 'm.s.': 4, 'm.a.': 4,
            'bachelor': 3, 'b.s.': 3, 'b.a.': 3,
            'associate': 2,
            'diploma': 1, 'certificate': 1
        }
        
        # Find candidate's highest education level
        candidate_level = 0
        for edu_type, level in education_levels.items():
            if edu_type in candidate_edu_lower:
                candidate_level = max(candidate_level, level)
        
        # Find required education level
        required_level = 0
        for edu_type, level in education_levels.items():
            if edu_type in job_lower:
                required_level = max(required_level, level)
        
        if required_level == 0:
            return 0.7  # Good default score if no education requirement specified
        
        if candidate_level >= required_level:
            return 1.0
        elif candidate_level == required_level - 1:
            return 0.8  # Close match
        else:
            return 0.4  # Significant gap
    
    def calculate_keyword_match(self, candidate_text: str, job_requirements: str) -> float:
        """Calculate general keyword matching score using TF-IDF-like approach"""
        candidate_words = self.preprocess_text(candidate_text)
        job_words = self.preprocess_text(job_requirements)
        
        if not candidate_words or not job_words:
            return 0.0
        
        # Count word frequencies
        candidate_freq = Counter(candidate_words)
        job_freq = Counter(job_words)
        
        # Calculate intersection
        common_words = set(candidate_words) & set(job_words)
        
        if not common_words:
            return 0.0
        
        # Calculate weighted score based on word importance in job description
        score = 0.0
        total_weight = 0.0
        
        for word in common_words:
            # Weight by frequency in job description (more frequent = more important)
            job_weight = job_freq[word]
            candidate_weight = candidate_freq[word]
            
            # TF-IDF-like scoring
            word_score = min(candidate_weight, job_weight) / job_weight
            score += word_score * job_weight
            total_weight += job_weight
        
        return score / total_weight if total_weight > 0 else 0.0
    
    def calculate_matching_score(self, candidate_data: Dict, job_data: Dict) -> float:
        """Calculate overall matching score between candidate and job"""
        
        # Extract relevant data
        candidate_skills = candidate_data.get('skills', [])
        candidate_experience = candidate_data.get('total_experience_years')
        candidate_education = candidate_data.get('education')
        candidate_text = candidate_data.get('parsed_cv_text', '')
        
        job_requirements = job_data.get('requirements', '')
        job_description = job_data.get('description', '')
        job_text = f"{job_requirements} {job_description}"
        
        # Calculate individual scores
        skills_score = self.calculate_skills_match(candidate_skills, job_text)
        experience_score = self.calculate_experience_match(candidate_experience, job_text)
        education_score = self.calculate_education_match(candidate_education, job_text)
        keyword_score = self.calculate_keyword_match(candidate_text, job_text)
        
        # Calculate weighted overall score
        overall_score = (
            skills_score * self.weights['skills_match'] +
            experience_score * self.weights['experience_match'] +
            education_score * self.weights['education_match'] +
            keyword_score * self.weights['keyword_match']
        )
        
        # Ensure score is between 0 and 1
        overall_score = max(0.0, min(1.0, overall_score))
        
        return round(overall_score, 3)
    
    def get_match_details(self, candidate_data: Dict, job_data: Dict) -> Dict:
        """Get detailed breakdown of matching scores"""
        candidate_skills = candidate_data.get('skills', [])
        candidate_experience = candidate_data.get('total_experience_years')
        candidate_education = candidate_data.get('education')
        candidate_text = candidate_data.get('parsed_cv_text', '')
        
        job_requirements = job_data.get('requirements', '')
        job_description = job_data.get('description', '')
        job_text = f"{job_requirements} {job_description}"
        
        skills_score = self.calculate_skills_match(candidate_skills, job_text)
        experience_score = self.calculate_experience_match(candidate_experience, job_text)
        education_score = self.calculate_education_match(candidate_education, job_text)
        keyword_score = self.calculate_keyword_match(candidate_text, job_text)
        overall_score = self.calculate_matching_score(candidate_data, job_data)
        
        return {
            'overall_score': overall_score,
            'breakdown': {
                'skills_match': round(skills_score, 3),
                'experience_match': round(experience_score, 3),
                'education_match': round(education_score, 3),
                'keyword_match': round(keyword_score, 3)
            },
            'weights': self.weights
        }

