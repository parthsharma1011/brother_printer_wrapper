#!/bin/bash
# Script to initialize git repository and push to GitHub

set -e

echo "🚀 Initializing Git Repository for Brother QL-700 Label Printer"
echo "=============================================================="

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
else
    echo "📁 Git repository already exists"
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Brother QL-700 Label Printer Web Interface

Features:
- Modern web interface with responsive design
- CSV upload and column selection
- Live label preview with QR codes
- Automatic printer detection
- Real-time progress tracking
- Command-line interface for batch printing
- Cross-platform support (Linux, macOS, Windows)
- Comprehensive error handling and logging
- Security-focused with input validation
- Clean, documented codebase ready for production

Tech stack: Python, Flask, Brother QL library, HTML5, CSS3, JavaScript"

# Add remote origin
echo "🔗 Adding GitHub remote..."
git remote remove origin 2>/dev/null || true
git remote add origin git@github.com:parthsharma1011/brother_printer_wrapper.git

# Create and switch to main branch
git branch -M main

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "🌐 Repository: https://github.com/parthsharma1011/brother_printer_wrapper"
echo ""
echo "📋 Next steps:"
echo "   1. Visit the GitHub repository"
echo "   2. Add a description and topics"
echo "   3. Enable GitHub Pages if desired"
echo "   4. Set up branch protection rules"
echo ""