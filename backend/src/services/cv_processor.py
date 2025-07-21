import re
import json
from typing import Dict, List, Optional
import os

class CVProcessor:
    """Service for processing and extracting information from CV text"""
    
    def __init__(self):
        self.skills_keywords = [
            # Programming languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css',
            
            # Frameworks and libraries
            'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node.js', 'laravel',
            'rails', 'asp.net', 'jquery', 'bootstrap', 'tensorflow', 'pytorch', 'pandas', 'numpy',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite',
            
            # Cloud and DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'gitlab', 'github',
            'terraform', 'ansible', 'linux', 'unix',
            
            # Other technical skills
            'machine learning', 'artificial intelligence', 'data science', 'big data', 'blockchain',
            'cybersecurity', 'network security', 'project management', 'agile', 'scrum', 'devops'
        ]
    
    def extract_contact_info(self, cv_text: str) -> Dict[str, Optional[str]]:
        """Extract contact information from CV text"""
        contact_info = {
            'email': None,
            'phone': None,
            'linkedin': None
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, cv_text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Extract phone number (various formats)
        phone_patterns = [
            r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',  # US format
            r'\+?([0-9]{1,4})[-.\s]?([0-9]{3,4})[-.\s]?([0-9]{3,4})[-.\s]?([0-9]{3,4})',  # International
            r'\b\d{10}\b'  # Simple 10-digit
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, cv_text)
            if phone_match:
                contact_info['phone'] = phone_match.group()
                break
        
        # Extract LinkedIn profile
        linkedin_pattern = r'linkedin\.com/in/([a-zA-Z0-9-]+)'
        linkedin_match = re.search(linkedin_pattern, cv_text, re.IGNORECASE)
        if linkedin_match:
            contact_info['linkedin'] = f"https://linkedin.com/in/{linkedin_match.group(1)}"
        
        return contact_info
    
    def extract_skills(self, cv_text: str) -> List[str]:
        """Extract skills from CV text"""
        cv_lower = cv_text.lower()
        found_skills = []
        
        for skill in self.skills_keywords:
            if skill.lower() in cv_lower:
                found_skills.append(skill.title())
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(found_skills))
    
    def extract_experience_years(self, cv_text: str) -> Optional[float]:
        """Extract total years of experience from CV text"""
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\+?\s*years?\s*experience',
            r'experience:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s*experience',
            r'(\d+)\+?\s*year\s*experience'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, cv_text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        # Try to infer from work history dates
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, cv_text)
        if len(years) >= 2:
            years = [int(year) for year in years]
            min_year = min(years)
            max_year = max(years)
            current_year = 2025  # Current year
            
            # Estimate experience as difference between earliest and current year
            if max_year >= current_year - 1:  # Recent work
                return float(current_year - min_year)
        
        return None
    
    def extract_education(self, cv_text: str) -> Optional[str]:
        """Extract education information from CV text"""
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'mba', 'degree',
            'university', 'college', 'institute', 'school',
            'b.s.', 'b.a.', 'm.s.', 'm.a.', 'ph.d.'
        ]
        
        lines = cv_text.split('\n')
        education_lines = []
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                education_lines.append(line.strip())
        
        return '\n'.join(education_lines) if education_lines else None
    
    def extract_name(self, cv_text: str) -> Dict[str, Optional[str]]:
        """Extract first and last name from CV text"""
        lines = cv_text.split('\n')
        
        # Usually the name is in the first few lines
        for line in lines[:5]:
            line = line.strip()
            if line and not any(char.isdigit() for char in line) and '@' not in line:
                # Remove common prefixes
                line = re.sub(r'^(mr\.?|ms\.?|mrs\.?|dr\.?)\s+', '', line, flags=re.IGNORECASE)
                
                # Split into words and take first two as first and last name
                words = line.split()
                if 2 <= len(words) <= 4:  # Reasonable name length
                    return {
                        'first_name': words[0],
                        'last_name': words[-1]
                    }
        
        return {'first_name': None, 'last_name': None}
    
    def process_cv(self, cv_text: str) -> Dict:
        """Process CV text and extract all relevant information"""
        contact_info = self.extract_contact_info(cv_text)
        name_info = self.extract_name(cv_text)
        skills = self.extract_skills(cv_text)
        experience_years = self.extract_experience_years(cv_text)
        education = self.extract_education(cv_text)
        
        return {
            'first_name': name_info['first_name'],
            'last_name': name_info['last_name'],
            'email': contact_info['email'],
            'phone': contact_info['phone'],
            'linkedin_profile': contact_info['linkedin'],
            'skills': skills,
            'total_experience_years': experience_years,
            'education': education,
            'parsed_cv_text': cv_text
        }

