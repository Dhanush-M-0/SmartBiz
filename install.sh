#!/bin/bash
# SmartBiz Installation Helper

echo "🔧 Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel -q

echo "📦 Installing SmartBiz dependencies..."
python -m pip install -r requirements.txt --only-binary :all:

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation successful!"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Setup Supabase tables (see SETUP_READY.md)"
    echo "2. Run: python main.py"
    echo "3. Open: http://localhost:5000"
else
    echo "❌ Installation failed. Try:"
    echo "python -m pip install --upgrade pip setuptools wheel"
    echo "pip install -r requirements.txt --no-build-isolation"
fi
