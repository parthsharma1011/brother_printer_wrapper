#!/bin/bash
# Brother QL-700 Label Printer Startup Script

echo "🏷️  Brother QL-700 Label Printer Web Interface"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "webapp/app.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start the application
echo "🚀 Starting application..."
cd webapp
python3 app.py