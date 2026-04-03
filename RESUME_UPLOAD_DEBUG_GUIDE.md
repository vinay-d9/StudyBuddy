# Resume Upload + AI Skill Extraction - Complete Debugging Guide

## Overview
This guide provides comprehensive debugging steps for the Resume Upload + AI Skill Extraction feature. It covers browser console debugging, backend logs, API testing, and step-by-step verification.

---

## Part 1: Quick Browser Verification

### Step 1: Open Browser Console
1. Open your app in Chrome/Firefox
2. Press `F12` or `Cmd+Option+I` (Mac) to open Developer Tools
3. Go to **Console** tab
4. You should see logs starting with: `🚀 Resume Modal System Loading...`

### Step 2: Check for Initialization Logs
Look for these success indicators:
```
🎯 ResumeModal.init() - Starting initialization...
📱 DOM is ready, initializing elements...
✅ Modal elements found: { overlay: true, modal: true }
🔗 Setting up event listeners...
   ✅ Close button listener attached
   ✅ YES button listener attached
   ✅ NO button listener attached
   ✅ Upload button listener attached
   ✅ File input change listener attached
```

### Step 3: Check API Call Logs
The console should show:
```
🔍 Checking for existing resume...
   Fetching /api/resume/latest...
   API Response status: 200
   API Response data: { resume: null }
   User has existing resume: false
   📝 No existing resume found - will show modal after delay
```

### Step 4: Manual Modal Test
1. Refresh the page
2. After ~1 second, the resume modal should appear
3. You should see: `👁️ Showing resume modal...`

---

## Part 2: Network Tab Debugging

### Check API Calls
1. In DevTools, go to **Network** tab
2. Reload page
3. Look for these calls:
   - `resume/latest` - Should return `200` with `{ resume: null }` or resume data

### Test Upload
1. Click "Yes, let's go" button
2. Select a PDF/DOCX file
3. Click "Upload & Extract Skills"
4. In Network tab, look for:
   - `POST /api/resume/upload` - Should return `200` with `{ id: <number>, filename: "...", content: "...", message: "..." }`
   - `POST /api/resume/extract-skills` - Should return `200` with skills

---

## Part 3: Backend Server Logs

### Enable Flask Debugging
1. Check that your Flask app is running with:
   ```bash
   python run.py
   ```
2. Watch for logs starting with `🎯 POST /api/resume/extract-skills`

### Expected Log Output
When uploading, you should see something like:
```
======================================================================
🎯 POST /api/resume/extract-skills - Handler called
======================================================================
📧 User email: user@example.com
📄 Resume ID from request: 42
📂 Fetching resume by ID: 42
✅ Resume found: resume.pdf
📝 Resume content length: 2543 chars
✅ OpenAI API key found
🔍 Calling OpenAI API for skill extraction...
✅ Groq API call succeeded
🧠 OpenAI response (first 200 chars): python, java, sql, javascript, react, ...
✅ Extracted 12 skills: [...]
======================================================================
```

### Check for Common Errors
Look for these error patterns:
- ❌ `Resume not found` - Resume wasn't saved to database
- ❌ `OpenAI API key not configured` - Environment variable not set
- ❌ `No skills extracted` - API response parsing failed
- ❌ `Could not extract text from file` - PDF/file parsing issue

---

## Part 4: File Upload Testing

### Test Each File Type
1. **PDF files**: Try uploading a PDF resume
   - Console should show: `📄 File selected: resume.pdf`
   - If PDF parsing fails, try a different PDF tool
   
2. **DOCX files**: Try uploading a Word document
   - Requires `python-docx` library
   - Console should show: `📄 File selected: resume.docx`

3. **TXT files**: Try uploading a plain text resume
   - Simplest format, good for testing

### File Validation
- Max file size: **10MB**
- Allowed extensions: **PDF, DOCX, DOC, TXT**
- Console will show: `❌ File too large (max 10MB)` if invalid

---

## Part 5: Manual API Testing (Using cURL)

### Test 1: Check Latest Resume
```bash
curl http://localhost:5000/api/resume/latest \
  -H "Cookie: session=<your-session-id>"
```

Expected response:
```json
{
  "resume": null
}
```

Or if resume exists:
```json
{
  "resume": {
    "id": 1,
    "filename": "resume.pdf",
    "ats_score": 75,
    "created_at": "2024-01-15 10:30:00"
  }
}
```

### Test 2: Upload Resume
```bash
curl -X POST http://localhost:5000/api/resume/upload \
  -F "file=@/path/to/resume.pdf" \
  -H "Cookie: session=<your-session-id>"
```

Expected response:
```json
{
  "id": 1,
  "filename": "resume.pdf",
  "content": "John Doe\n123 Main St\n...",
  "message": "Resume uploaded successfully"
}
```

### Test 3: Extract Skills
```bash
curl -X POST http://localhost:5000/api/resume/extract-skills \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<your-session-id>" \
  -d '{"resume_id": 1}'
```

Expected response:
```json
{
  "success": true,
  "skills_extracted": 12,
  "skills": ["python", "java", "sql", "javascript", "react"],
  "message": "Successfully extracted 12 skills...",
  "checklist": { "groups": [...] }
}
```

---

## Part 6: Database Verification

### Check if Resume Saved
```bash
cd prepfriend
sqlite3 data/database.db
```

Then run:
```sql
SELECT * FROM resumes ORDER BY created_at DESC LIMIT 1;
```

You should see the resume you uploaded.

### Check Skill Checklist
```sql
SELECT email, data FROM skill_checklists WHERE email = 'your@email.com';
```

The JSON should contain a "Resume Skills" group with extracted skills.

---

## Part 7: Environment Variable Troubleshooting

### Check if GROQ_API_KEY is Set
```bash
echo $GROQ_API_KEY
```

If empty:
```bash
export GROQ_API_KEY="your-groq-api-key"
```

### Check if Key is Valid
The API key should start with: `gsk_`

### Test API Key Directly
```bash
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

---

## Part 8: Common Issues & Solutions

### Issue 1: Modal Never Shows
**Symptoms**: Resume modal doesn't appear on dashboard

**Solutions**:
1. Check console for: `🎯 ResumeModal.init() - Starting initialization...`
2. Verify file exists: `/app/static/js/resume-modal.js`
3. Verify CSS file exists: `/app/static/css/resume-modal.css`
4. Check if user already has a resume: `SELECT * FROM resumes WHERE email = 'your@email.com'`

### Issue 2: Upload Button Does Nothing
**Symptoms**: Clicking upload doesn't trigger any action

**Solutions**:
1. Check console for: `🚀 Upload button clicked`
2. Verify file is selected: Console should show `📄 File selected: filename`
3. Look for validation errors: `❌ File too large` or similar
4. Check Network tab for POST requests

### Issue 3: "Skill Extraction Failed"
**Symptoms**: Upload works but skill extraction fails

**Solutions**:
1. Check if GROQ_API_KEY is set:
   ```bash
   python -c "import os; print(os.environ.get('GROQ_API_KEY'))"
   ```
2. Look for in server logs: `❌ Groq API error: ...`
3. Test API directly:
   ```bash
   curl https://api.groq.com/openai/v1/models \
     -H "Authorization: Bearer $GROQ_API_KEY"
   ```
4. Check if rate limited: `"429"` in response

### Issue 4: PDF Parsing Fails
**Symptoms**: Error like "Could not extract text from PDF"

**Solutions**:
1. Check if PyPDF2 is installed:
   ```bash
   python -c "import PyPDF2; print('OK')"
   ```
2. Try installing: `pip install PyPDF2 pdfplumber`
3. Test with simpler PDF or TXT file
4. Check for: `No extractable text found in PDF. It may be a scanned image`

### Issue 5: DOCX Upload Fails
**Symptoms**: Error with .docx files

**Solutions**:
1. Check if python-docx is installed:
   ```bash
   python -c "from docx import Document; print('OK')"
   ```
2. Install: `pip install python-docx`
3. Verify file is not corrupted: Try opening in Word
4. Server logs should show: `❌ DOCX extraction failed for filename`

---

## Part 9: Complete Testing Checklist

### ✅ Frontend
- [ ] Modal appears 1 second after page load
- [ ] "Yes, let's go" button shows upload form
- [ ] "Not right now" button closes modal
- [ ] Close (×) button closes modal
- [ ] File input shows file validation
- [ ] Upload button disabled until file selected
- [ ] Status messages appear (loading, success, error)
- [ ] Modal closes after successful upload
- [ ] Page reloads after upload completes

### ✅ Backend
- [ ] POST `/api/resume/upload` returns 200 with resume ID
- [ ] Resume stored in database with email
- [ ] File saved to disk at `/data/resumes/<email>/<filename>`
- [ ] POST `/api/resume/extract-skills` returns skills list
- [ ] Skills added to skill checklist
- [ ] GET `/api/resume/latest` returns latest resume

### ✅ API Integration
- [ ] GROQ_API_KEY environment variable set
- [ ] OpenAI client initialized with Groq base URL
- [ ] Skill extraction API call succeeds
- [ ] Response parsing doesn't error on unexpected format
- [ ] Rate limiting handled gracefully

### ✅ Database
- [ ] Resumes table has proper schema
- [ ] Resume records saved with email and timestamp
- [ ] Skill checklist JSON valid
- [ ] Resume skills group created in checklist
- [ ] Skills deduplicated (no duplicates)

---

## Part 10: Debug Mode Setup

### Enable Verbose Logging
Add this to your Flask app initialization:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Browser Console Tips
1. Keep console open while testing
2. All logs prefixed with emoji for quick scanning
3. Copy entire log for troubleshooting

### Enable JavaScript Debugging
1. In DevTools Console, set breakpoints:
   ```javascript
   debugger;  // Add in code to pause execution
   ```
2. Use conditional breakpoints on Network requests
3. Watch specific variables in Scope panel

---

## Part 11: Performance Debugging

### Check Request Times
In Network tab, look for:
- `/api/resume/upload` - Should complete in < 3 seconds
- `/api/resume/extract-skills` - Should complete in < 5 seconds (API call)

Too slow? Check:
- File size (max 10MB)
- Network connectivity
- Server resources (CPU, memory)
- Groq API response time

### Monitor Database Queries
```bash
sqlite3 data/database.db ".mode line"
SELECT * FROM resumes;
```

---

## Part 12: Testing with Sample Files

### Create Test Resume (TXT)
```bash
cat > test_resume.txt << 'EOF'
JOHN DOE
123 Main Street
Phone: (555) 123-4567
Email: john@example.com

TECHNICAL SKILLS
- Programming Languages: Python, Java, JavaScript, C++
- Web Frameworks: React, Django, Node.js
- Databases: PostgreSQL, MongoDB, MySQL
- Tools: Git, Docker, Kubernetes, AWS
- Methodologies: Agile, Scrum, TDD

EXPERIENCE
Senior Software Engineer at Tech Corp
- Developed APIs using Python and Django
- Managed PostgreSQL databases
- Led Agile team of 5 developers

EDUCATION
B.S. Computer Science
State University
EOF
```

### Expected Skills Extracted
Python, Java, JavaScript, C++, React, Django, Node.js, PostgreSQL, MongoDB, MySQL, Git, Docker, Kubernetes, AWS

---

## Part 13: Reset & Clean Testing

### Clear Session Data
```javascript
// In browser console:
sessionStorage.clear();
localStorage.clear();
location.reload();
```

### Reset Database Resume
```sql
DELETE FROM resumes WHERE email = 'your@email.com';
DELETE FROM skill_checklists WHERE email = 'your@email.com';
```

### Clear Uploads Folder
```bash
rm -rf prepfriend/data/resumes/your_at_example.com/*
```

---

## Getting Help

### When Reporting Issues
Include:
1. **Browser console output** (copy entire logs)
2. **Server logs** (last 50 lines when error occurred)
3. **Network tab** (screenshot showing POST requests)
4. **Expected vs actual behavior**
5. **Steps to reproduce**

### Verification Commands
Before reporting issues, run:
```bash
# Check API key
echo $GROQ_API_KEY

# Check dependencies
python -c "import PyPDF2, docx; print('Dependencies OK')"

# Check database
sqlite3 prepfriend/data/database.db "SELECT COUNT(*) as resume_count FROM resumes;"

# Check Flask app
python -c "from app import app; print('Flask app loads OK')"
```

---

## Version Info

- Frontend: JavaScript (ES6+)
- Backend: Flask with SQLite
- AI API: Groq (OpenAI-compatible)
- Resume Parsing: PyPDF2, pdfplumber, python-docx
- Database: SQLite3

---

Last Updated: 2024
For latest updates, check the main README.md
