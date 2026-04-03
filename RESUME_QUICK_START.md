# 🎯 RESUME FEATURE - QUICK SETUP GUIDE

## Status
✅ **All files are in place**
✅ **Database is initialized**  
✅ **Dependencies are installed**
❌ **API Key needs to be set**

---

## 🚀 What You Need to Do RIGHT NOW

### Step 1: Get API Key (2 minutes)
1. Go to: https://console.groq.com
2. Sign up (free) or log in
3. Create API key
4. Copy the key (starts with `gsk_`)

### Step 2: Set Environment Variable

#### Option A: For This Session Only
```bash
export GROQ_API_KEY="gsk_your_key_here"
python3 run.py
```

#### Option B: Permanently (Recommended)
```bash
# Add to ~/.zshrc
echo 'export GROQ_API_KEY="gsk_your_key_here"' >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Verify it worked
echo $GROQ_API_KEY  # Should print your key
```

### Step 3: Start the App
```bash
cd /Users/vinay/Documents/prep/prepfriend
python3 run.py
```

### Step 4: Test the Feature
1. Open http://localhost:5001
2. Log in or register
3. Go to Dashboard
4. **You should see the resume modal asking "Do you have your resume?"**
5. Click "Yes, let's go"
6. Upload a test resume
7. AI extracts skills automatically ✨

---

## ✨ What the Feature Does

When you upload a resume:
1. **File is uploaded** to `/data/resumes/<email>/resume.pdf`
2. **Text is extracted** from PDF/DOCX/DOC/TXT
3. **AI analyzes content** using Groq API
4. **Skills are extracted** (Python, Java, SQL, etc.)
5. **Checklist is updated** with new "Resume Skills" group
6. **Each skill becomes a task** you can track

---

## 🔍 Troubleshooting

### Modal doesn't appear?
1. **Clear browser cache**: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
2. **Check console logs**: F12 > Console tab
3. **Look for 🎯 emoji** in logs

### Upload fails?
1. **Check file format**: Supported are PDF, DOCX, DOC, TXT
2. **Check file size**: Max 10MB
3. **Check server logs**: Look for error messages

### "Skill extraction failed"?
1. **Verify API key is set**: `echo $GROQ_API_KEY`
2. **Make sure it starts with**: `gsk_`
3. **Restart Flask app**: Press Ctrl+C and run `python3 run.py` again

### "Cannot connect to localhost:5001"?
1. **Flask might be running on different port**
2. **Check terminal output** for "Running on http://..."
3. **Try http://localhost:5000** instead

---

## 📋 Verification Checklist

- [ ] Python dependencies installed (Flask, OpenAI, PyPDF2, python-docx)
- [ ] GROQ_API_KEY environment variable set (`echo $GROQ_API_KEY`)
- [ ] Database exists (`ls -lh data/studybuddy.db`)
- [ ] All feature files in place
- [ ] App starting without errors (`python3 run.py`)
- [ ] Modal appears on dashboard
- [ ] Can upload a resume file
- [ ] Skills are extracted and shown

---

## 📂 File Locations

Resume feature files are at:
```
prepfriend/
├── app/
│   ├── static/
│   │   ├── js/resume-modal.js ............ Modal logic
│   │   └── css/resume-modal.css ......... Modal styling
│   ├── templates/
│   │   └── dashboard.html .............. Modal HTML
│   ├── routes.py ...................... API endpoints
│   └── db.py .......................... Database functions
│
└── data/
    └── studybuddy.db .................. Database (with resumes table)
```

---

## 🆘 Still Having Issues?

1. Run diagnostic:
   ```bash
   python3 resume_diagnostic.py
   ```

2. Check all prerequisites are met
3. Look at Flask server output for errors
4. Check browser console (F12) for JavaScript errors

---

## ✅ Next Steps

1. Set GROQ_API_KEY (see Step 2 above)
2. Run: `python3 run.py`
3. Open: http://localhost:5001
4. Test the resume upload feature
5. Enjoy AI-powered skill extraction! 🎉

---

**Last Updated:** April 4, 2026
