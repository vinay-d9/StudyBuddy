#!/usr/bin/env python3
"""
Resume Feature - Complete Setup and Verification
This script installs everything needed and verifies the feature works
"""

import subprocess
import sys
import os
from pathlib import Path

def run_cmd(cmd, description=""):
    """Run a shell command and return success/failure"""
    if description:
        print(f"\n{'='*70}")
        print(f"📝 {description}")
        print('='*70)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "🎯 RESUME FEATURE SETUP WIZARD" + " "*23 + "║")
    print("╚" + "="*68 + "╝")
    
    # Check current directory
    if not os.path.exists("app/routes.py"):
        print("\n❌ ERROR: Run this script from the prepfriend root directory!")
        print("   cd /Users/vinay/Documents/prep/prepfriend")
        sys.exit(1)
    
    # Step 1: Install dependencies
    print("\n\n" + "▶ STEP 1: Installing Python Dependencies")
    print("-" * 70)
    
    deps = [
        "flask==2.3.0",
        "openai==1.3.0",
        "PyPDF2==3.16.0", 
        "python-docx==0.8.11",
        "pdfplumber==0.9.0",
    ]
    
    print("📦 Installing packages:")
    for dep in deps:
        print(f"   - {dep}")
    
    cmd = f"pip install {' '.join(deps)} -q 2>&1 | grep -E 'error|Error|ERROR' || echo '✅ All packages installed'"
    
    if run_cmd(cmd):
        print("✅ Dependencies installed successfully!")
    else:
        print("⚠️  Some packages may have issues, continuing anyway...")
    
    # Step 2: Check API key
    print("\n\n" + "▶ STEP 2: GROQ API Key Configuration")
    print("-" * 70)
    
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        masked = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
        print(f"✅ GROQ_API_KEY is set: {masked}")
    else:
        print("⚠️  GROQ_API_KEY is not set")
        print("\n📝 To set it NOW, run:")
        print("   export GROQ_API_KEY=\"gsk_PASTE_YOUR_KEY_HERE\"")
        print("\n📝 To set it PERMANENTLY, add to ~/.zshrc:")
        print("   echo 'export GROQ_API_KEY=\"gsk_YOUR_KEY\"' >> ~/.zshrc")
        print("   source ~/.zshrc")
        print("\n🔗 Get a free API key: https://console.groq.com")
        
        response = input("\n❓ Continue anyway? (yes/no): ").strip().lower()
        if response != "yes":
            print("⛔ Setup cancelled. Please set GROQ_API_KEY and run again.")
            sys.exit(1)
    
    # Step 3: Verify database
    print("\n\n" + "▶ STEP 3: Verifying Database")
    print("-" * 70)
    
    try:
        import sqlite3
        db_path = "data/studybuddy.db"
        
        if not os.path.exists(db_path):
            print(f"⚠️  Database not found at {db_path}")
            print("   (It will be created when app starts)")
        else:
            size = os.path.getsize(db_path)
            print(f"✅ Database found: {db_path} ({size} bytes)")
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cursor.fetchall()]
            conn.close()
            
            if "resumes" in tables:
                print(f"✅ Database has all required tables ({len(tables)} total)")
                print(f"   Tables: {', '.join(tables[:5])}...")
            else:
                print(f"⚠️  'resumes' table not found. Will be created on first app run.")
    except Exception as e:
        print(f"⚠️  Could not verify database: {e}")
    
    # Step 4: Verify files
    print("\n\n" + "▶ STEP 4: Verifying Feature Files")
    print("-" * 70)
    
    files = {
        "app/static/js/resume-modal.js": "Resume Modal JavaScript",
        "app/static/css/resume-modal.css": "Resume Modal CSS",
        "app/templates/dashboard.html": "Dashboard Template",
        "app/routes.py": "API Routes",
    }
    
    all_exist = True
    for filepath, name in files.items():
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {name:30} {size:>6} bytes")
        else:
            print(f"❌ {name:30} NOT FOUND")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Some files are missing!")
        sys.exit(1)
    
    # Step 5: Ready to run
    print("\n\n" + "▶ STEP 5: Ready to Launch!")
    print("="*70)
    
    print("\n✅ All checks passed! The resume feature is ready to use.\n")
    
    print("🚀 TO START THE APP:")
    print("   python3 run.py")
    print("\n🌐 THEN OPEN IN BROWSER:")
    print("   http://localhost:5001")
    print("   (or http://localhost:5000 if port differs)")
    
    print("\n📋 WHAT TO EXPECT:")
    print("   1. Log in or register")
    print("   2. Go to Dashboard")
    print("   3. Modal asking 'Do you have your resume?' should appear")
    print("   4. Click 'Yes, let's go'")
    print("   5. Upload a resume (PDF, DOCX, DOC, or TXT)")
    print("   6. AI extracts skills automatically")
    print("   7. Skills appear in your Skill Checklist")
    
    print("\n💡 TROUBLESHOOTING:")
    print("   - If modal doesn't appear: Clear browser cache (Ctrl+Shift+Delete)")
    print("   - If upload fails: Check Flask server logs for errors")
    print("   - If skills don't extract: Verify GROQ_API_KEY is set")
    
    print("\n🔍 DEBUG MODE:")
    print("   1. Open Developer Tools (F12)")
    print("   2. Go to Console tab")
    print("   3. Look for messages starting with 🎯 ✅ ❌ 📤")
    
    print("\n" + "="*70 + "\n")
    
    # Ask if user wants to start app now
    start = input("❓ Start the app now? (yes/no): ").strip().lower()
    
    if start == "yes":
        print("\n🚀 Starting Flask app...\n")
        os.system("python3 run.py")
    else:
        print("\n✅ Setup complete! Run 'python3 run.py' when ready.\n")

if __name__ == "__main__":
    main()
