# Resume Upload Feature - Quick Start Checklist

## Pre-Flight Checklist (Before Starting)

Run this command to verify everything:
```bash
python3 test_resume_system.py
```

### Expected Results ✅
- ✓ JavaScript files present
- ✓ Backend routes defined
- ✓ Database connectivity working
- ✓ All required methods in place

### Current Issues ⚠️
- API key needs to be set
- Dependencies may need installation
- Database tables need initialization

---

## Setup Checklist (Do These Now)

### Step 1: Environment Variables
- [ ] Obtain Groq API key from https://console.groq.com
- [ ] Set API key:
  ```bash
  export GROQ_API_KEY="gsk_your_key_here"
  ```
- [ ] Verify it's set:
  ```bash
  echo $GROQ_API_KEY  # Should show your key
  ```

### Step 2: Dependencies
- [ ] CD to prepfriend directory:
  ```bash
  cd prepfriend
  ```
- [ ] Install required packages:
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Or install individually:
  ```bash
  pip install flask openai PyPDF2 python-docx pdfplumber
  ```
- [ ] Verify installations:
  ```bash
  python3 -c "from flask import Flask; from openai import OpenAI; print('OK')"
  ```

### Step 3: Database
- [ ] Start the application:
  ```bash
  python3 run.py
  ```
- [ ] Wait for "Running on http://localhost:5000"
- [ ] Verify database tables were created:
  ```bash
  sqlite3 data/database.db ".tables"
  ```
- [ ] Should see tables including: resumes, skill_checklists, users

### Step 4: Verify Setup
- [ ] Run test suite again:
  ```bash
  python3 test_resume_system.py
  ```
- [ ] Check for "All tests passed" or >80% success rate

---

## Feature Testing Checklist

### Browser Tests
- [ ] Open http://localhost:5000 in browser
- [ ] Log in or register
- [ ] Open Dashboard
- [ ] Resume modal should appear within 1 second
- [ ] Look at browser console (F12) for logs starting with 🎯

### Upload Test
- [ ] Create a test resume file (resume.txt):
  ```
  John Doe
  Phone: 123-456-7890
  Email: john@example.com
  
  Skills: Python, Java, JavaScript, SQL
  Experience: Django development
  ```
- [ ] Click "Yes, let's go" button
- [ ] Select your test resume
- [ ] Click "Upload & Extract Skills"
- [ ] Should see success message

### Verification
- [ ] After upload, page reloads
- [ ] Go to "Skill Checklist" section
- [ ] Should see "Resume Skills" group
- [ ] Should see extracted skills (Python, Java, JavaScript, SQL, etc.)

### Server Logs
- [ ] Watch Flask server logs during upload
- [ ] Should see lines like:
  ```
  🎯 POST /api/resume/extract-skills - Handler called
  ✅ Groq API call succeeded
  ✅ Extracted 12 skills
  ```

---

## File Checklist (Already in Place ✓)

### Frontend Files ✓
- ✓ `/app/static/js/resume-modal.js` - Modal JavaScript (14KB)
- ✓ `/app/static/css/resume-modal.css` - Modal styling (6KB)
- ✓ `/app/templates/dashboard.html` - Contains modal HTML (12KB)

### Backend Files ✓
- ✓ `/app/routes.py` - Contains all API endpoints
  - ✓ POST /api/resume/upload
  - ✓ POST /api/resume/extract-skills
  - ✓ GET /api/resume/latest
- ✓ `/app/db.py` - Database functions
  - ✓ save_resume()
  - ✓ get_latest_resume()
  - ✓ get_skill_checklist()
  - ✓ save_skill_checklist()

### Documentation Files ✓
- ✓ `RESUME_UPLOAD_DEBUG_GUIDE.md` - Comprehensive troubleshooting
- ✓ `RESUME_SETUP_GUIDE.md` - Complete setup instructions
- ✓ `test_resume_system.py` - Automated testing script

---

## Common Issues & Quick Fixes

### Issue: Modal Doesn't Appear
**Fix:** Check browser console (F12) for errors
- If "resume-modal-overlay not found" → Clear cache
- If "fetch error" → Check if API key is set

### Issue: "Skill Extraction Failed"
**Fix:** 
1. Verify API key: `echo $GROQ_API_KEY`
2. Make sure it starts with `gsk_`
3. Restart Flask: Press Ctrl+C and run `python3 run.py` again

### Issue: Upload Fails
**Fix:**
1. Check file size (max 10MB)
2. Use supported format (PDF, DOCX, or TXT)
3. Try with simple TXT file first
4. Check server logs for specific error

### Issue: Database Table Missing
**Fix:**
1. Stop Flask app (Ctrl+C)
2. Delete `/data/database.db`
3. Restart Flask: `python3 run.py`
4. Database will auto-create

---

## Commands Reference

### Quick Setup
```bash
cd prepfriend
export GROQ_API_KEY="your-key"
pip install -r requirements.txt
python3 run.py
```

### Testing
```bash
python3 test_resume_system.py
```

### Troubleshooting
```bash
# Check API key
echo $GROQ_API_KEY

# Test dependencies
python3 -c "import flask, openai, PyPDF2; print('OK')"

# Check database
sqlite3 data/database.db "SELECT COUNT(*) FROM resumes;"

# View Flask logs (while running)
tail -f logs/flask.log  # if logging file exists
```

---

## What Gets Created When You Upload

1. **File saved to disk:**
   ```
   /data/resumes/<email>/<filename>
   ```

2. **Resume record in database:**
   ```sql
   INSERT INTO resumes (email, filename, file_content, ...)
   ```

3. **Skills extracted and saved:**
   ```sql
   UPDATE skill_checklists 
   SET data = JSON with new "Resume Skills" group
   WHERE email = user_email
   ```

4. **Checklist updated in UI:**
   - "Resume Skills" group appears in checklist
   - Each skill becomes a task: "Master {Skill}"
   - Tasks show source: "From your resume"

---

## Next Steps After Setup

### For Users
1. Upload your actual resume
2. Skills get auto-extracted
3. Resume skills appear in checklist
4. Track progress on skill mastery
5. Use checklist for interview prep

### For Developers
1. Customize skill extraction prompt in `routes.py` line 1691
2. Modify skill group structure as needed
3. Add resume analysis features (ATS score, etc.)
4. Integrate with interview prep modules

---

## Success Indicators

**You'll know it's working when:**

1. ✅ Resume modal appears on dashboard
2. ✅ Upload completes without errors
3. ✅ Browser console shows extraction logs
4. ✅ Server logs show "✅ Extracted skills"
5. ✅ Skills appear in "Resume Skills" checklist group
6. ✅ Each skill shows "From your resume" metadata

---

## Support Resources

### Documentation Files
- `RESUME_UPLOAD_DEBUG_GUIDE.md` - Deep troubleshooting
- `RESUME_SETUP_GUIDE.md` - Complete setup instructions
- `README.md` - Project overview

### Test Suite
Run anytime to verify system health:
```bash
python3 test_resume_system.py
```

### Quick Diagnostics
```bash
#!/bin/bash
echo "=== Environment ==="
echo "API Key: $(echo $GROQ_API_KEY | cut -c1-8)..."
echo "Working dir: $(pwd)"
echo ""
echo "=== Dependencies ==="
pip list | grep -E "flask|openai|PyPDF2"
echo ""
echo "=== Database ==="
sqlite3 prepfriend/data/database.db "SELECT COUNT(*) as resume_count FROM resumes;" 2>/dev/null || echo "Database not initialized"
```

---

## Timeline

- **5 min:** Install dependencies + set API key
- **2 min:** Initialize database (start app once)
- **2 min:** Run test suite
- **5 min:** Manual testing in browser
- **✓ Done!** Feature is live

---

## Version Info

- **Frontend:** ES6+ JavaScript with comprehensive logging
- **Backend:** Flask + SQLite  
- **AI:** Groq API (OpenAI-compatible)
- **File Parsing:** PyPDF2, pdfplumber, python-docx
- **Status:** ✅ Ready for deployment

---

**Next:** Follow RESUME_SETUP_GUIDE.md for detailed instructions

**Questions?** Check RESUME_UPLOAD_DEBUG_GUIDE.md for comprehensive troubleshooting
