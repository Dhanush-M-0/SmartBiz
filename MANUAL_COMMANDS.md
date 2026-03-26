# 🚀 SmartBiz Installation - Direct Commands

Copy and paste these commands in your terminal one by one:

---

## **Command 1: Upgrade pip tools** (30-60 seconds)

```bash
python -m pip install --upgrade pip setuptools wheel
```

Expected output: Successfully installed...

---

## **Command 2: Try installing with binary wheels** (2-5 minutes)

```bash
pip install -r requirements.txt --only-binary :all:
```

**If this works,** go to "Verification" section below.

**If you get pandas errors,** run Command 3.

---

## **Command 3: Alternative method (if Command 2 failed)**

```bash
pip install -r requirements.txt --prefer-binary
```

**If this works,** go to "Verification" section below.

**If this also fails,** run Command 4.

---

## **Command 4: Last resort (if Command 3 failed)**

```bash
pip install -r requirements-minimal.txt
```

This lets pip choose compatible versions automatically.

---

## **Verification: Check if installation worked**

```bash
python -c "import flask; import supabase; import pandas; print('✅ All imports successful!')"
```

Expected output:
```
✅ All imports successful!
```

---

## **Next Steps (After Verification)**

1. **Setup Supabase Tables:**
   - Open SETUP_READY.md
   - Copy SQL from DATABASE_SETUP.sql
   - Paste into Supabase SQL Editor
   - Run the SQL

2. **Run SmartBiz:**
   ```bash
   python main.py
   ```

3. **Access:**
   Open your browser: http://localhost:5000

---

## 🆘 If none of the commands work:

Try creating a fresh virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

**Pick Command 2 first. If it fails, try 3, then 4. Let me know which one works!**
