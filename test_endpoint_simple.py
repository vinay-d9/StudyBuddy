#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, '/Users/vinay/Documents/prep/prepfriend')

from app import create_app
from app.db import save_resume

app = create_app()
client = app.test_client()

test_email = "test@example.com"
db_path = app.config["DATABASE"]

# Add test resume
test_content = "John Doe\njohn@example.com\nPROFESSIONAL SUMMARY\nExperienced software engineer with 5+ years using Python, JavaScript, React.\nTECHNICAL SKILLS\nPython, JavaScript, Java, SQL, React, Node.js, Docker, Kubernetes, Git, AWS\nWORK EXPERIENCE\nSenior Software Engineer at Tech Corp 2022-Present\nProjects section on github.com/johndoe\nEDUCATION\nBS Computer Science 2018"

save_resume(db_path, test_email, "test_resume.txt", test_content)

# Test endpoint
with client:
    with client.session_transaction() as sess:
        sess["user_email"] = test_email
    
    response = client.post("/api/resume/extract-skills", json={})
    
    print(f"Status: {response.status_code}")
    try:
        data = response.get_json()
        if response.status_code == 200:
            print("✅ SUCCESS")
            print(json.dumps(data, indent=2))
        else:
            print("❌ ERROR")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Failed to parse: {e}")
        print(f"Response: {response.data}")
