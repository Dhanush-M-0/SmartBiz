#!/bin/bash
set -e

echo "🚀 SmartBiz Startup Script"
echo "=========================="

# Check Python version
echo "✓ Checking Python..."
python --version

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your Supabase credentials:"
    echo "   - SUPABASE_URL"
    echo "   - SUPABASE_KEY"
    echo "   - EMAIL_ADDRESS (for notifications)"
    echo "   - EMAIL_PASSWORD"
    exit 1
fi

echo "✓ Configuration file found"

# Start Flask server
echo ""
echo "🌐 Starting SmartBiz Flask Server..."
echo "📍 Access at: http://localhost:5000"
echo "🔴 Press Ctrl+C to stop"
echo ""

python main.py
