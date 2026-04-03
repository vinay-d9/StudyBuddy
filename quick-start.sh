#!/bin/bash
# RESUME FEATURE - MINIMUM STEPS TO GET WORKING
# Copy and paste these commands exactly

echo "🎯 RESUME FEATURE - QUICK START"
echo "================================"
echo ""

# Step 1: Verify we're in the right place
if [ ! -f "app/routes.py" ]; then
    echo "❌ ERROR: Run this from /Users/vinay/Documents/prep/prepfriend"
    echo "   cd /Users/vinay/Documents/prep/prepfriend"
    exit 1
fi

echo "✅ In correct directory"
echo ""

# Step 2: Check if API key is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ GROQ_API_KEY is not set!"
    echo ""
    echo "📝 To set it, copy ONE of these:"
    echo ""
    echo "Temporary (this session only):"
    echo "  export GROQ_API_KEY=\"gsk_PASTE_YOUR_KEY_HERE\""
    echo ""
    echo "Permanent (recommended):"
    echo "  echo 'export GROQ_API_KEY=\"gsk_PASTE_YOUR_KEY_HERE\"' >> ~/.zshrc"
    echo "  source ~/.zshrc"
    echo ""
    echo "🔗 Get free API key: https://console.groq.com"
    echo ""
    exit 1
fi

echo "✅ GROQ_API_KEY is set"
echo ""

# Step 3: Verify dependencies
echo "Checking dependencies..."
python3 -c "import flask, openai; print('✅ Flask and OpenAI installed')" 2>/dev/null || {
    echo "❌ Dependencies missing, installing..."
    pip install flask openai PyPDF2 python-docx -q
    echo "✅ Dependencies installed"
}

echo ""
echo "═════════════════════════════════════════"
echo "🚀 READY TO START!"
echo "═════════════════════════════════════════"
echo ""
echo "Run this to start the app:"
echo "  python3 run.py"
echo ""
echo "Then open in browser:"
echo "  http://localhost:5001"
echo ""
echo "You should see the resume modal on the dashboard!"
echo ""
