#!/bin/bash
# Resume Feature Quick-Fix Script
# This installs everything needed and sets up the feature properly

set -e  # Exit on any error

echo "=================================="
echo "🚀 RESUME FEATURE SETUP"
echo "=================================="
echo ""

# 1. Install dependencies
echo "📦 Installing Python dependencies..."
pip install flask==2.3.0 openai==1.3.0 PyPDF2==3.16.0 python-docx==0.8.11 -q
echo "✅ Dependencies installed"
echo ""

# 2. Set API key
echo "🔑 Checking GROQ API key..."
if [ -z "$GROQ_API_KEY" ]; then
    echo "⚠️  GROQ_API_KEY not set"
    echo ""
    echo "📝 To set it, run:"
    echo "   export GROQ_API_KEY=\"gsk_your_api_key\""
    echo ""
    echo "Get key from: https://console.groq.com"
    echo ""
else
    masked=$(echo "$GROQ_API_KEY" | cut -c1-4)...$(echo "$GROQ_API_KEY" | cut -c-4)
    echo "✅ API Key is set: $masked"
fi

# 3. Initialize database
echo "💾 Initializing database..."
python3 -c "
import sys
sys.path.insert(0, '.')
from app.db import init_db
from app import app

with app.app_context():
    init_db(app.config['DATABASE'])
print('✅ Database initialized')
" 2>/dev/null || echo "⚠️  Could not auto-initialize database (will be created on app start)"

echo ""
echo "=================================="
echo "✅ SETUP COMPLETE!"
echo "=================================="
echo ""
echo "🚀 TO START THE APP:"
echo "   python3 run.py"
echo ""
echo "🌐 THEN OPEN:"
echo "   http://localhost:5000"
echo ""
echo "📋 FEATURES:"
echo "   ✓ Resume upload modal will appear on dashboard"
echo "   ✓ Upload PDF/DOCX/DOC/TXT resume"
echo "   ✓ AI extracts skills automatically"
echo "   ✓ Skills added to checklist"
echo ""
echo "💡 TIP: Make sure to clear browser cache (Ctrl+Shift+Delete)"
echo "        if modal doesn't appear!"
echo ""
