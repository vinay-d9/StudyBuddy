# Resume Upload + AI Skill Extraction - Setup & Deployment Guide

## Current Status

The test suite shows that:
- ✅ **Frontend is ready** (HTML, CSS, JavaScript files are in place)
- ✅ **Backend routes are defined** (upload, extract-skills endpoints)
- ⚠️ **Missing dependencies** (Flask, OpenAI, parsing libraries)
- ⚠️ **Missing API key** (GROQ_API_KEY not set)
- ⚠️ **Database not initialized** (resumes table missing)

---

## Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
cd prepfriend

# Install Python dependencies
pip install -r requirements.txt

# Or install individually if needed:
pip install flask openai PyPDF2 python-docx pdfplumber
```

### Step 2: Set API Key
```bash
# On macOS/Linux:
export GROQ_API_KEY="your-groq-api-key-here"

# Or add to ~/.zshrc or ~/.bash_profile for persistence:
echo 'export GROQ_API_KEY="your-groq-api-key-here"' >> ~/.zshrc
source ~/.zshrc

# Verify it's set:
echo $GROQ_API_KEY
```

### Step 3: Initialize Database
```bash
# Run the app once to initialize database
python3 run.py

# The database will be created with all tables
# Check that data/database.db exists:
ls -la prepfriend/data/database.db
```

### Step 4: Verify Setup
```bash
python3 test_resume_system.py

# You should see "All tests passed!" or high success rate
```

---

## Detailed Setup Instructions

### Option A: First Time Setup

#### 1. Check Python Version
```bash
python3 --version
# Should be 3.8+
```

#### 2. Create Virtual Environment (Recommended)
```bash
cd prepfriend
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# source venv\Scripts\activate  # On Windows
```

#### 3. Install Dependencies
```bash
# From prepfriend directory
pip install --upgrade pip
pip install -r requirements.txt
```

**If requirements.txt is missing or incomplete:**
```bash
pip install flask==2.3.0
pip install flask-session==0.5.0
pip install openai==1.3.0
pip install PyPDF2==3.16.0
pip install python-docx==0.8.11
pip install pdfplumber==0.9.0
pip install requests==2.31.0
pip install python-dotenv==1.0.0
```

#### 4. Obtain Groq API Key
1. Visit https://console.groq.com
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

#### 5. Set Environment Variables
```bash
# Temporary (for current session only):
export GROQ_API_KEY="gsk_your_actual_key_here"

# Permanent (add to shell profile):
nano ~/.zshrc  # or ~/.bash_profile for bash

# Add this line:
export GROQ_API_KEY="gsk_your_actual_key_here"

# Save and reload:
source ~/.zshrc

# Verify:
echo $GROQ_API_KEY  # Should print your key
```

#### 6. Run Application
```bash
# From prepfriend root directory
python3 run.py

# Or specify port:
python3 run.py --port 5000
```

#### 7. Test in Browser
1. Open: http://localhost:5000
2. Log in or register
3. Go to dashboard
4. Resume modal should appear
5. Test upload with a sample resume

---

### Option B: Update Existing Setup

If you already have the app running but resume feature doesn't work:

#### 1. Update Dependencies
```bash
pip install --upgrade openai PyPDF2 python-docx pdfplumber
```

#### 2. Verify API Key
```bash
# Check if set:
echo $GROQ_API_KEY

# If not set, add it:
export GROQ_API_KEY="gsk_your_key_here"
```

#### 3. Restart Application
```bash
# Kill existing process:
# Press Ctrl+C in terminal

# Restart:
python3 run.py
```

#### 4. Clear Browser Cache
```bash
# Press Ctrl+Shift+Delete (Windows/Linux)
# Or Cmd+Shift+Delete (Mac)

# Or in Chrome DevTools:
# Right-click > Empty cache and hard refresh
```

---

## Testing the Setup

### Run Test Suite
```bash
python3 test_resume_system.py

# Expected output:
# ✓ All tests passed! System is ready.
# Or high success rate (>80%)
```

### Manual Browser Testing

#### Test 1: Modal Appears
1. Open dashboard
2. Should see resume modal within 1 second
3. Check console (F12) for logs starting with 🎯

#### Test 2: Upload Works
1. Click "Yes, let's go"
2. Select a test resume file
3. Click "Upload & Extract Skills"
4. Should see success message

#### Test 3: Skills Extracted
1. After upload completes
2. Check console for extracted skills
3. Should see something like: `✅ Extracted 12 skills: [python, java, ...]`

#### Test 4: Checklist Updated
1. After upload completes, page reloads
2. Go to Skill Checklist section
3. Should see "Resume Skills" group with extracted skills

### Server Log Inspection
While testing, watch server logs for patterns:

**Success pattern:**
```
🎯 POST /api/resume/extract-skills - Handler called
✅ Resume found: resume.pdf
✅ Groq API call succeeded
✅ Extracted 12 skills
```

**Error pattern:**
```
❌ GROQ_API_KEY not configured
❌ Resume not found
❌ Could not extract text from file
```

---

## Troubleshooting

### Issue: API Key Not Recognized

**Solution:**
```bash
# Verify key format:
echo $GROQ_API_KEY | head -c 4  # Should print: gsk_

# If empty, set it:
export GROQ_API_KEY="gsk_your_key"

# Add to permanent location:
echo 'export GROQ_API_KEY="gsk_your_key"' >> ~/.zshrc
source ~/.zshrc
```

### Issue: PyPDF2 Missing

**Solution:**
```bash
pip install PyPDF2

# Test:
python3 -c "import PyPDF2; print('OK')"
```

### Issue: Database Table Missing

**Solution:**
```bash
# Initialize database:
python3 run.py

# Check if table exists:
sqlite3 prepfriend/data/database.db ".tables"

# Should see: resumes, skill_checklists, users, ...
```

### Issue: Modal Never Appears

**Solution:**
1. Check console (F12) for error messages
2. Verify file exists: `prepfriend/app/static/js/resume-modal.js`
3. Check Network tab for 404 errors
4. Clear cache: Ctrl+Shift+Delete

### Issue: Upload Fails

**Solution:**
1. Check file size (max 10MB)
2. Use supported format (PDF, DOCX, DOC, TXT)
3. Check server logs for specific error
4. Try with simple TXT file first

### Issue: "Skill Extraction Failed"

**Solution:**
1. Verify GROQ_API_KEY is set: `echo $GROQ_API_KEY`
2. Check API key is valid (starts with `gsk_`)
3. Test API directly:
   ```bash
   curl https://api.groq.com/openai/v1/models \
     -H "Authorization: Bearer $GROQ_API_KEY"
   ```
4. Check if API is rate limited or experiencing issues
5. Try again after a few seconds

---

## Production Deployment

### For Deployment to Heroku/Railway/Cloud

#### 1. Set Environment Variables
```bash
# Via CLI:
heroku config:set GROQ_API_KEY="gsk_your_key"

# Via dashboard:
# Settings > Config Vars > Add GROQ_API_KEY

# Verification:
heroku config  # See all variables
```

#### 2. Ensure Dependencies
```bash
# Verify requirements.txt includes:
cat requirements.txt | grep -E "flask|openai|PyPDF2|python-docx"
```

#### 3. Database Setup
```bash
# Most cloud platforms auto-run migrations
# Verify database exists after first deployment

# Check on deployed app:
# API call should work: GET /api/resume/latest
```

#### 4. Logging
```python
# Configure logging for troubleshooting:
import logging
logging.basicConfig(level=logging.INFO)

# Check deployment logs:
heroku logs --tail
railway logs
```

---

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GROQ_API_KEY=${GROQ_API_KEY}

CMD ["python3", "run.py"]
```

### Build and Run
```bash
docker build -t prepfriend .
docker run -e GROQ_API_KEY="gsk_your_key" -p 5000:5000 prepfriend
```

---

## Performance Optimization

### Caching Resume Extraction
```python
# Cache extracted skills to avoid re-processing
CACHE_TIMEOUT = 24 * 3600  # 24 hours

# In extract_skills_from_resume():
cache_key = f"skills_{resume_id}"
cached = cache.get(cache_key)
if cached:
    return cached
```

### Database Indexes
```sql
-- Add indexes for faster queries
CREATE INDEX idx_resumes_email ON resumes(email);
CREATE INDEX idx_resumes_created ON resumes(created_at DESC);
CREATE INDEX idx_skill_checklists_email ON skill_checklists(email);
```

---

## Monitoring & Logs

### View Real-Time Logs
```bash
# Terminal:
tail -f server.log

# Or use Flask logger:
import logging
logger = logging.getLogger(__name__)
logger.info("Resume uploaded")
```

### Database Diagnostics
```bash
cd prepfriend

# Check resumes count:
sqlite3 data/database.db "SELECT COUNT(*) as total_resumes FROM resumes;"

# See latest resumes:
sqlite3 data/database.db "SELECT filename, created_at FROM resumes ORDER BY created_at DESC LIMIT 5;"

# Check database size:
ls -lh data/database.db
```

### API Diagnostics
```bash
# Test endpoints directly:

# Check latest resume:
curl http://localhost:5000/api/resume/latest \
  -H "Cookie: session=<your-session>"

# Check Groq API:
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY" | jq '.data | length'
```

---

## Quick Reference

### Commands Cheat Sheet
```bash
# Setup
export GROQ_API_KEY="your-key"
pip install -r requirements.txt
python3 run.py

# Testing
python3 test_resume_system.py

# Database
sqlite3 prepfriend/data/database.db ".tables"

# Logs
tail -f server.log

# Diagnostics
echo $GROQ_API_KEY
pip list | grep -E "flask|openai|PyPDF2"
```

### Useful URLs
- **Groq Console:** https://console.groq.com
- **Groq Docs:** https://groq.com/docs
- **OpenAI Compatibility:** https://groq.com/docs/openai-compatibility
- **Python Packages:** https://pypi.org

---

## Getting Help

### Debug Information to Include
When reporting issues, provide:
1. Python version: `python3 --version`
2. Installed packages: `pip list`
3. Environment: `echo $GROQ_API_KEY` (first 4 chars)
4. OS: `uname -a` (macOS/Linux)
5. Browser: Chrome/Firefox version
6. Error logs: Browser console + server logs

### Test Script Output
```bash
python3 test_resume_system.py
# Copy entire output when troubleshooting
```

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Set GROQ_API_KEY
3. ✅ Run application
4. ✅ Test in browser
5. ✅ Run test_resume_system.py
6. ✅ Check all tests pass
7. ✅ Deploy to production

---

**Last Updated:** 2024
**For more help:** See RESUME_UPLOAD_DEBUG_GUIDE.md
