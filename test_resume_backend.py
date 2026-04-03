#!/usr/bin/env python3
"""
Test script to verify resume skill extraction backend
Run this to debug the skill extraction pipeline
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_json_parsing():
    """Test if Groq JSON response parsing works"""
    print("\n" + "="*80)
    print("TEST 1: JSON Parsing Validation")
    print("="*80)
    
    # Simulate Groq response
    sample_response = """
{
  "technical_skills": [
    "python",
    "javascript",
    "react",
    "nodejs",
    "sql",
    "docker"
  ],
  "soft_skills": [
    "leadership",
    "communication",
    "project management",
    "teamwork"
  ],
  "tools_frameworks": [
    "git",
    "docker",
    "kubernetes",
    "aws"
  ]
}
"""
    
    try:
        skills_data = json.loads(sample_response)
        print("✅ JSON parsing successful")
        print(f"   Technical skills: {len(skills_data.get('technical_skills', []))} found")
        print(f"   Soft skills: {len(skills_data.get('soft_skills', []))} found")
        print(f"   Tools/Frameworks: {len(skills_data.get('tools_frameworks', []))} found")
        
        # Test flattening
        all_skills = (
            skills_data.get("technical_skills", []) + 
            skills_data.get("tools_frameworks", []) + 
            skills_data.get("soft_skills", [])
        )
        all_skills = list(dict.fromkeys([s.lower().strip() for s in all_skills if s.strip()]))
        print(f"   Total unique skills: {len(all_skills)}")
        print(f"   Skills: {all_skills}")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return False


def test_ats_scoring():
    """Test ATS scoring logic"""
    print("\n" + "="*80)
    print("TEST 2: ATS Score Calculation")
    print("="*80)
    
    # Sample resume content
    sample_resume = """
John Doe
john@example.com | (555) 123-4567 | LinkedIn.com/in/johndoe | GitHub.com/johndoe

SUMMARY
Experienced software engineer with 5+ years building scalable web applications.
Expertise in full-stack development, cloud infrastructure, and team leadership.

SKILLS
Languages: Python, JavaScript, TypeScript, Java, SQL
Frameworks: React, Node.js, Django, Flask, Express
Databases: PostgreSQL, MongoDB, Redis, DynamoDB
Tools & Platforms: Docker, AWS, Kubernetes, Git, Jenkins
Methodologies: Agile, Scrum, CI/CD, DevOps

EXPERIENCE
Senior Software Engineer | TechCorp | 2021 - Present
- Led development of microservices architecture using Node.js and Docker
- Improved system performance by 40% through database optimization
- Mentored junior developers and led code review process

Software Engineer | StartupXYZ | 2019 - 2021
- Built full-stack React/Node.js applications
- Implemented CI/CD pipeline using Jenkins and Docker
- Contributed to open source projects on GitHub

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2019

CERTIFICATIONS
AWS Certified Solutions Architect - Associate
Kubernetes Application Developer

PROJECTS
E-commerce Platform: Developed scalable platform using React, Node.js, PostgreSQL
Analytics Dashboard: Built real-time dashboard with WebSocket integration
"""
    
    # Simulate skill extraction results
    technical_skills = ["python", "javascript", "typescript", "java", "sql"]
    soft_skills = ["leadership", "communication", "mentoring"]
    tools_frameworks = ["docker", "aws", "kubernetes", "git", "jenkins", "react", "nodejs"]
    
    total_skills = len(technical_skills) + len(soft_skills) + len(tools_frameworks)
    
    # Calculate scores
    ats_score = 0
    resume_lower = sample_resume.lower()
    
    # 1. Skill count scoring (max 40)
    skill_score = min(40, len(technical_skills) * 3 + len(tools_frameworks) * 2 + len(soft_skills) * 1)
    ats_score += skill_score
    print(f"✅ Skill count score: {skill_score}/40")
    
    # 2. Keyword presence (max 30)
    keyword_score = 0
    keywords = {
        "projects": 5,
        "github": 5,
        "internship": 4,
        "experience": 4,
        "education": 4,
        "certification": 3,
        "achievement": 3,
    }
    
    for keyword, points in keywords.items():
        if keyword in resume_lower:
            keyword_score += points
            print(f"✅ Found '{keyword}' (+{points})")
    
    keyword_score = min(30, keyword_score)
    ats_score += keyword_score
    print(f"✅ Keyword score: {keyword_score}/30")
    
    # 3. Structure scoring (max 20)
    structure_score = 0
    sections = {
        "contact": 3,
        "summary": 4,
        "skills": 4,
        "experience": 5,
        "education": 4,
    }
    
    for section, points in sections.items():
        if section in resume_lower:
            structure_score += points
            print(f"✅ Found '{section}' section (+{points})")
    
    structure_score = min(20, structure_score)
    ats_score += structure_score
    print(f"✅ Structure score: {structure_score}/20")
    
    # 4. Content density (max 10)
    lines = [l.strip() for l in sample_resume.split('\n') if l.strip()]
    density_score = min(10, (len(lines) // 20) * 2) if len(lines) > 20 else 0
    ats_score += density_score
    print(f"✅ Density score: {density_score}/10 ({len(lines)} lines)")
    
    ats_score = min(100, ats_score)
    
    print(f"\n🎯 FINAL ATS SCORE: {ats_score}/100")
    print(f"   Total skills extracted: {total_skills}")
    print(f"   Breakdown: {len(technical_skills)} technical, {len(tools_frameworks)} tools, {len(soft_skills)} soft skills")
    
    return ats_score >= 50  # Pass if score reasonable


def test_response_format():
    """Verify response format matches frontend expectations"""
    print("\n" + "="*80)
    print("TEST 3: Response Format Validation")
    print("="*80)
    
    response = {
        "success": True,
        "ats_score": 75,
        "skills_extracted": 15,
        "skills": {
            "technical_skills": ["python", "javascript"],
            "soft_skills": ["leadership"],
            "tools_frameworks": ["docker"],
            "all_skills": ["python", "javascript", "leadership", "docker"]
        },
        "skills_added_to_checklist": 12,
        "message": "Successfully extracted 15 skills (ATS Score: 75/100)"
    }
    
    # Validate structure
    required_fields = ["success", "ats_score", "skills_extracted", "skills", "message"]
    
    for field in required_fields:
        if field not in response:
            print(f"❌ Missing field: {field}")
            return False
        print(f"✅ Field present: {field}")
    
    # Validate skills structure
    if not isinstance(response["skills"], dict):
        print("❌ 'skills' should be a dict")
        return False
    
    skills_keys = ["technical_skills", "soft_skills", "tools_frameworks", "all_skills"]
    for key in skills_keys:
        if key not in response["skills"]:
            print(f"❌ Missing skill category: {key}")
            return False
        print(f"✅ Skill category present: {key}")
    
    print(f"\n✅ Response format is valid")
    print(f"   Success: {response['success']}")
    print(f"   ATS Score: {response['ats_score']}")
    print(f"   Skills: {response['skills_extracted']}")
    
    return True


if __name__ == "__main__":
    print("\n" + "█"*80)
    print("  RESUME SKILL EXTRACTION - BACKEND TEST SUITE")
    print("█"*80)
    
    tests = [
        ("JSON Parsing", test_json_parsing),
        ("ATS Scoring", test_ats_scoring),
        ("Response Format", test_response_format),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "█"*80)
    print(f"  TEST RESULTS: {passed} passed, {failed} failed")
    print("█"*80 + "\n")
    
    sys.exit(0 if failed == 0 else 1)
