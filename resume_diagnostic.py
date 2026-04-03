#!/usr/bin/env python3
"""
Resume Feature Diagnostic - Check what's actually happening
"""

import os
import sys

print("\n" + "="*70)
print("🔍 RESUME FEATURE DIAGNOSTIC")
print("="*70 + "\n")

# 1. Check files exist
print("1️⃣  CHECKING FILES...")
files_to_check = [
    "app/static/js/resume-modal.js",
    "app/static/css/resume-modal.css",
    "app/templates/dashboard.html",
]

for f in files_to_check:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"   ✅ {f} ({size} bytes)")
    else:
        print(f"   ❌ {f} NOT FOUND")

# 2. Check routes.py for endpoints
print("\n2️⃣  CHECKING ROUTES...")
with open("app/routes.py", "r") as f:
    content = f.read()
    
endpoints = [
    "/api/resume/upload",
    "/api/resume/extract-skills",
    "/api/resume/latest",
]

for ep in endpoints:
    if f'@main.route("{ep}"' in content:
        print(f"   ✅ Route {ep} exists")
    else:
        print(f"   ❌ Route {ep} NOT FOUND")

# 3. Check if resume-modal.js is being loaded
print("\n3️⃣  CHECKING DASHBOARD TEMPLATE...")
with open("app/templates/dashboard.html", "r") as f:
    dashboard = f.read()

if 'id="resume-modal-overlay"' in dashboard:
    print("   ✅ Modal HTML element found")
else:
    print("   ❌ Modal HTML element NOT FOUND")

if 'resume-modal.js' in dashboard:
    print("   ✅ resume-modal.js is referenced in template")
else:
    print("   ❌ resume-modal.js NOT referenced in template")

if 'resume-modal.css' in dashboard:
    print("   ✅ resume-modal.css is referenced in template")
else:
    print("   ❌ resume-modal.css NOT referenced in template")

# 4. Check database
print("\n4️⃣  CHECKING DATABASE...")
db_path = "data/database.db"
if os.path.exists(db_path):
    size = os.path.getsize(db_path)
    print(f"   ✅ Database exists ({size} bytes)")
    
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"   ✅ Database has {len(tables)} tables:")
        for table in tables:
            print(f"      - {table[0]}")
        conn.close()
    except Exception as e:
        print(f"   ❌ Error reading database: {e}")
else:
    print(f"   ⚠️  Database not found at {db_path}")
    print("      (Will be created when app runs for first time)")

# 5. Check environment
print("\n5️⃣  CHECKING ENVIRONMENT...")
api_key = os.environ.get("GROQ_API_KEY")
if api_key:
    masked = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
    print(f"   ✅ GROQ_API_KEY set: {masked}")
else:
    print("   ⚠️  GROQ_API_KEY not set (needed for skill extraction)")

# 6. Check dependencies
print("\n6️⃣  CHECKING DEPENDENCIES...")
try:
    import flask
    print("   ✅ flask installed")
except:
    print("   ❌ flask NOT installed")

try:
    from openai import OpenAI
    print("   ✅ openai installed")
except:
    print("   ❌ openai NOT installed")

try:
    import PyPDF2
    print("   ✅ PyPDF2 installed")
except:
    print("   ⚠️  PyPDF2 not installed (optional, for PDF parsing)")

try:
    from docx import Document
    print("   ✅ python-docx installed")
except:
    print("   ⚠️  python-docx not installed (optional, for DOCX parsing)")

# 7. Check if modal is properly implemented
print("\n7️⃣  CHECKING MODAL IMPLEMENTATION...")
with open("app/static/js/resume-modal.js", "r") as f:
    js_content = f.read()

checks = [
    ("class ResumeModal", "Class definition"),
    ("new ResumeModal()", "Class instantiation"),
    ("checkSessionAndShow", "Session check method"),
    ("fetch('/api/resume/latest')", "API call"),
    ("console.log", "Logging"),
]

for check, label in checks:
    if check in js_content:
        print(f"   ✅ {label}")
    else:
        print(f"   ❌ {label} NOT FOUND")

print("\n" + "="*70)
print("✅ DIAGNOSTIC COMPLETE")
print("="*70 + "\n")

print("📋 SUMMARY:")
print("-" * 70)
print("If everything shows ✅, the feature should work!")
print("If something shows ❌, that needs to be fixed.")
print("If something shows ⚠️ , that's optional but might be needed.")
print("\n💡 TIP: After fixing issues, RESTART the Flask app and")
print("   CLEAR BROWSER CACHE (Ctrl+Shift+Delete)")
print("-" * 70 + "\n")
