#!/bin/bash

# Zeta AI Backend Startup Script

echo "🚀 Starting Zeta AI Backend..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✏️  Please edit .env and add your GEMINI_API_KEY"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run application
echo "✅ Starting Flask application..."
python app.py
