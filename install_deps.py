#!/usr/bin/env python3
"""
SmartBiz Dependency Installer
Handles common installation issues across different Python versions
"""

import subprocess
import sys
import os

def run_command(cmd, description=""):
    """Run a shell command and handle errors"""
    if description:
        print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ Success")
            return True
        else:
            print(f"❌ Failed")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print("⏱️  Timeout - installation took too long")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🚀 SmartBiz Dependency Installer")
    print("=" * 60)
    
    # Check Python version
    print(f"\n📌 Python Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Step 1: Upgrade pip, setuptools, wheel
    print("\n" + "=" * 60)
    print("Step 1: Upgrading pip, setuptools, wheel")
    print("=" * 60)
    
    run_command(
        "python -m pip install --upgrade pip setuptools wheel",
        "Upgrading pip and build tools"
    )
    
    # Step 2: Try installing with binary wheels only
    print("\n" + "=" * 60)
    print("Step 2: Installing dependencies (Method 1: Binary only)")
    print("=" * 60)
    
    if run_command(
        "pip install -r requirements.txt --only-binary :all: -q",
        "Installing from pre-built wheels"
    ):
        print("\n✅ Installation successful!")
        verify_installation()
        return
    
    # Step 3: Try with --prefer-binary
    print("\n" + "=" * 60)
    print("Step 2: Installing dependencies (Method 2: Prefer binary)")
    print("=" * 60)
    
    if run_command(
        "pip install -r requirements.txt --prefer-binary -q",
        "Installing with binary preference"
    ):
        print("\n✅ Installation successful!")
        verify_installation()
        return
    
    # Step 4: Try minimal requirements
    print("\n" + "=" * 60)
    print("Step 3: Installing minimal requirements (Method 3)")
    print("=" * 60)
    
    if run_command(
        "pip install -r requirements-minimal.txt -q",
        "Installing minimal dependencies"
    ):
        print("\n✅ Installation successful!")
        verify_installation()
        return
    
    # Step 5: Try --no-build-isolation
    print("\n" + "=" * 60)
    print("Step 4: Installing with no build isolation (Method 4)")
    print("=" * 60)
    
    if run_command(
        "pip install -r requirements.txt --no-build-isolation -q",
        "Installing without build isolation"
    ):
        print("\n✅ Installation successful!")
        verify_installation()
        return
    
    print("\n" + "=" * 60)
    print("❌ Installation failed with all methods")
    print("=" * 60)
    print("\n📖 See INSTALL_HELP.md for manual installation steps")
    sys.exit(1)

def verify_installation():
    """Verify that key packages are installed"""
    print("\n" + "=" * 60)
    print("📋 Verifying Installation")
    print("=" * 60)
    
    packages = [
        ('Flask', 'Flask'),
        ('supabase', 'supabase'),
        ('pandas', 'pandas'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('schedule', 'schedule'),
        ('click', 'Click'),
    ]
    
    all_success = True
    for import_name, display_name in packages:
        try:
            __import__(import_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name}")
            all_success = False
    
    if all_success:
        print("\n✨ All packages installed successfully!")
        print("\n🚀 Next steps:")
        print("1. Setup Supabase tables (see SETUP_READY.md)")
        print("2. Run: python main.py")
        print("3. Open: http://localhost:5000")
    else:
        print("\n⚠️  Some packages failed to verify")
        sys.exit(1)

if __name__ == '__main__':
    main()
