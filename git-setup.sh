#!/bin/bash

# Intervals.icu Activity Tracker - Git Setup Script

echo "🚀 Initializing Git repository..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "ℹ️  Git repository already exists"
fi

# Add all files
git add .

# Create initial commit
echo ""
echo "Creating initial commit..."
git commit -m "Initial commit: Intervals.icu Activity Tracker

- FastAPI backend with REST API
- SQLite database with SQLAlchemy
- Intervals.icu API integration
- Automated background sync scheduler
- Web interface with activity table
- Sortable columns and filtering
- Date range selection for sync
- Docker support for deployment
- Ready for cloud deployment (Railway, Render, Fly.io)"

echo ""
echo "✅ Initial commit created!"
echo ""
echo "📋 Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Add the remote:"
echo "   git remote add origin YOUR_GITHUB_REPO_URL"
echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo "4. Deploy to cloud (see DEPLOYMENT.md)"
echo ""
echo "🌟 Recommended: Deploy to Railway.app for free hosting!"
