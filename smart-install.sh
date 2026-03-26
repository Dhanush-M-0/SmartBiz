#!/bin/bash
# SmartBiz Smart Installation Script

set -e

echo "=========================================="
echo "🚀 SmartBiz Smart Installer"
echo "=========================================="
echo ""

# Function to print status
print_step() {
    echo ""
    echo "=========================================="
    echo "📍 $1"
    echo "=========================================="
}

# Function to print success
print_success() {
    echo "✅ $1"
}

# Function to print failure
print_failure() {
    echo "❌ $1"
}

# Check Python version
print_step "Checking Python Version"
PYTHON_VERSION=$(python --version 2>&1)
echo "Version: $PYTHON_VERSION"

# Step 1: Upgrade pip, setuptools, wheel
print_step "Step 1/4: Upgrading pip, setuptools, and wheel"
python -m pip install --upgrade pip setuptools wheel --quiet 2>&1 | tail -3 || true
print_success "Pip tools updated"

# Step 2: Try binary-only installation
print_step "Step 2/4: Installing dependencies (Method 1: Binary wheels only)"
if pip install -r requirements.txt --only-binary :all: --quiet 2>&1; then
    print_success "Installation succeeded!"
    METHOD="Method 1 (Binary only)"
else
    echo "⚠️  Binary-only failed, trying alternative method..."
    
    # Step 3: Try prefer-binary
    print_step "Step 3/4: Installing dependencies (Method 2: Prefer binary)"
    if pip install -r requirements.txt --prefer-binary --quiet 2>&1; then
        print_success "Installation succeeded!"
        METHOD="Method 2 (Prefer binary)"
    else
        echo "⚠️  Prefer-binary failed, trying alternative method..."
        
        # Step 4: Try no-build-isolation
        print_step "Step 4/4: Installing dependencies (Method 3: No build isolation)"
        if pip install -r requirements.txt --no-build-isolation --quiet 2>&1; then
            print_success "Installation succeeded!"
            METHOD="Method 3 (No build isolation)"
        else
            print_failure "All installation methods failed"
            echo ""
            echo "⚠️  Troubleshooting:"
            echo "1. Make sure you're in /workspaces/SmartBiz directory"
            echo "2. Try manually: pip install -r requirements-minimal.txt"
            echo "3. Check INSTALL_HELP.md for more options"
            exit 1
        fi
    fi
fi

# Verification
print_step "Verifying Installation"

VERIFY_RESULT=$(python -c "
import sys
packages = ['flask', 'supabase', 'pandas', 'requests', 'schedule', 'click']
failed = []
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg.capitalize()}')
    except ImportError as e:
        print(f'❌ {pkg.capitalize()}')
        failed.append(pkg)

if failed:
    sys.exit(1)
print('')
print('✨ All packages verified!')
" 2>&1)

echo "$VERIFY_RESULT"

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "🎉 SUCCESS! Installation Complete"
    echo "=========================================="
    echo ""
    echo "Installation Method: $METHOD"
    echo ""
    echo "🚀 Next Steps:"
    echo "1. Setup Supabase Tables (see SETUP_READY.md)"
    echo "2. Run: python main.py"
    echo "3. Open: http://localhost:5000"
    echo ""
    exit 0
else
    print_failure "Package verification failed"
    exit 1
fi
