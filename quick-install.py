#!/usr/bin/env python3
"""
SmartBiz One-Click Installer
Installs all dependencies with automatic error handling
"""

import subprocess
import sys

def install_all():
    """Install all requirements"""
    
    print("\n" + "="*60)
    print("🚀 SmartBiz One-Click Installer")
    print("="*60 + "\n")
    
    # Upgrade pip first
    print("📦 Step 1: Upgrading pip, setuptools, wheel...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", 
            "install", "--upgrade",
            "pip", "setuptools", "wheel",
            "-q"
        ])
        print("✅ Pip tools upgraded\n")
    except Exception as e:
        print(f"⚠️  Could not upgrade pip: {e}\n")
    
    # Install requirements
    print("📦 Step 2: Installing dependencies...")
    print("   This may take 2-5 minutes...\n")
    
    methods = [
        (["pip", "install", "-r", "requirements.txt", "--only-binary", ":all:"], "Method 1: Binary wheels only"),
        (["pip", "install", "-r", "requirements.txt", "--prefer-binary"], "Method 2: Prefer binary"),
        (["pip", "install", "-r", "requirements-minimal.txt"], "Method 3: Minimal requirements"),
        (["pip", "install", "-r", "requirements.txt"], "Method 4: Standard install"),
    ]
    
    for cmd, method_name in methods:
        try:
            print(f"   Trying {method_name}...")
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✅ {method_name} succeeded!\n")
            break
        except subprocess.CalledProcessError:
            print(f"   ⚠️  {method_name} failed, trying next...\n")
    else:
        print("❌ All installation methods failed!")
        sys.exit(1)
    
    # Verify installation
    print("📋 Step 3: Verifying installation...")
    
    packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'supabase': 'Supabase',
        'sqlalchemy': 'SQLAlchemy',
        'dotenv': 'Python-dotenv',
        'requests': 'Requests',
        'pandas': 'Pandas',
        'openpyxl': 'OpenPyXL',
        'schedule': 'Schedule',
        'click': 'Click',
    }
    
    failed = []
    for import_name, display_name in packages.items():
        try:
            __import__(import_name)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name}")
            failed.append(display_name)
    
    if failed:
        print(f"\n⚠️  Failed packages: {', '.join(failed)}")
        print("Try: pip install -r requirements-minimal.txt")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✨ Installation Complete!")
    print("="*60)
    print("\n🚀 Next steps:")
    print("   1. Setup Supabase tables (see SETUP_READY.md)")
    print("   2. Run: python main.py")
    print("   3. Open: http://localhost:5000\n")

if __name__ == "__main__":
    install_all()
