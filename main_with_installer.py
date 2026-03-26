"""
SmartBiz Flask Web Application
Auto-installs dependencies on first run
"""

import sys
import subprocess

# Auto-install dependencies if missing
def ensure_dependencies():
    """Install missing dependencies automatically"""
    required_modules = {
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
    
    print("\n" + "="*60)
    print("🔍 Checking dependencies...")
    print("="*60 + "\n")
    
    missing = []
    for module, name in required_modules.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} (missing)")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Found {len(missing)} missing package(s)")
        print("📦 Installing dependencies...\n")
        
        try:
            # Try methods in order
            methods = [
                ["pip", "install", "-r", "requirements.txt", "--only-binary", ":all:"],
                ["pip", "install", "-r", "requirements.txt", "--prefer-binary"],
                ["pip", "install", "-r", "requirements-minimal.txt"],
                ["pip", "install", "-r", "requirements.txt"],
            ]
            
            for i, cmd in enumerate(methods, 1):
                print(f"   Attempting method {i}...")
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ Installation succeeded with method {i}!\n")
                    return
                elif i < len(methods):
                    print(f"   ⚠️  Method failed, trying next...\n")
            
            print("❌ Installation failed with all methods")
            print("💡 Try manually: pip install -r requirements.txt")
            sys.exit(1)
            
        except Exception as e:
            print(f"❌ Error during installation: {str(e)}")
            sys.exit(1)
    
    print("\n✅ All dependencies installed!\n")

# Ensure dependencies are installed
ensure_dependencies()

# Now import Flask and other modules
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import logging
from config import Config, config
from database import get_db
from models import Employee, Task
from reports import get_report_generator
from notifications import get_notifier
from scheduler import get_scheduler
from datetime import datetime
import os

# Setup Flask app
app = Flask(__name__)
app.config.from_object(config.get('development'))
CORS(app)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize components
db = get_db()
notifier = get_notifier()
report_generator = get_report_generator()
scheduler = get_scheduler()

# ============== ROUTES - DASHBOARD ==============

@app.route('/')
def index():
    """Dashboard homepage"""
    return render_template('dashboard.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'SmartBiz is running'}), 200

# ============== ROUTES - EMPLOYEES ==============

@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Get all employees"""
    try:
        response = db.table('employees').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        logger.error(f"Failed to fetch employees: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees', methods=['POST'])
def create_employee():
    """Create a new employee"""
    try:
        data = request.json
        emp = Employee(
            name=data.get('name'),
            email=data.get('email'),
            department=data.get('department')
        )
        
        result = db.table('employees').insert(emp.to_dict()).execute()
        logger.info(f"Created employee: {data.get('name')}")
        return jsonify({'success': True, 'message': 'Employee created'}), 201
    except Exception as e:
        logger.error(f"Failed to create employee: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    """Get a specific employee"""
    try:
        response = db.table('employees').select('*').eq('id', emp_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'Employee not found'}), 404
    except Exception as e:
        logger.error(f"Failed to fetch employee: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    """Update an employee"""
    try:
        data = request.json
        db.table('employees').update(data).eq('id', emp_id).execute()
        logger.info(f"Updated employee {emp_id}")
        return jsonify({'success': True, 'message': 'Employee updated'}), 200
    except Exception as e:
        logger.error(f"Failed to update employee: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    """Delete an employee"""
    try:
        db.table('employees').delete().eq('id', emp_id).execute()
        logger.info(f"Deleted employee {emp_id}")
        return jsonify({'success': True, 'message': 'Employee deleted'}), 200
    except Exception as e:
        logger.error(f"Failed to delete employee: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ============== ROUTES - TASKS ==============

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        status_filter = request.args.get('status')
        
        query = db.table('tasks').select('*')
        if status_filter:
            query = query.eq('status', status_filter)
        
        response = query.execute()
        return jsonify(response.data), 200
    except Exception as e:
        logger.error(f"Failed to fetch tasks: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.json
        task = Task(
            title=data.get('title'),
            description=data.get('description'),
            assigned_to=data.get('assigned_to'),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date'),
            status='pending'
        )
        
        result = db.table('tasks').insert(task.to_dict()).execute()
        logger.info(f"Created task: {data.get('title')}")
        return jsonify({'success': True, 'message': 'Task created'}), 201
    except Exception as e:
        logger.error(f"Failed to create task: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    try:
        response = db.table('tasks').select('*').eq('id', task_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        logger.error(f"Failed to fetch task: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    try:
        data = request.json
        data['updated_at'] = datetime.utcnow().isoformat()
        db.table('tasks').update(data).eq('id', task_id).execute()
        logger.info(f"Updated task {task_id}")
        return jsonify({'success': True, 'message': 'Task updated'}), 200
    except Exception as e:
        logger.error(f"Failed to update task: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        db.table('tasks').delete().eq('id', task_id).execute()
        logger.info(f"Deleted task {task_id}")
        return jsonify({'success': True, 'message': 'Task deleted'}), 200
    except Exception as e:
        logger.error(f"Failed to delete task: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ============== ROUTES - REPORTS ==============

@app.route('/api/reports/task-summary', methods=['POST'])
def generate_task_report():
    """Generate task summary report"""
    try:
        filepath = report_generator.generate_task_summary_report()
        if filepath:
            return jsonify({'success': True, 'filepath': filepath}), 200
        return jsonify({'error': 'Failed to generate report'}), 500
    except Exception as e:
        logger.error(f"Failed to generate task report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/performance', methods=['POST'])
def generate_performance_report():
    """Generate employee performance report"""
    try:
        filepath = report_generator.generate_employee_performance_report()
        if filepath:
            return jsonify({'success': True, 'filepath': filepath}), 200
        return jsonify({'error': 'Failed to generate report'}), 500
    except Exception as e:
        logger.error(f"Failed to generate performance report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/currency', methods=['POST'])
def generate_currency_report():
    """Generate currency rates report"""
    try:
        currency = request.json.get('currency', 'USD')
        filepath = report_generator.generate_currency_rates_report(currency)
        if filepath:
            return jsonify({'success': True, 'filepath': filepath}), 200
        return jsonify({'error': 'Failed to generate report'}), 500
    except Exception as e:
        logger.error(f"Failed to generate currency report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/list', methods=['GET'])
def list_reports():
    """List all generated reports"""
    try:
        reports = report_generator.list_reports()
        return jsonify({'reports': reports}), 200
    except Exception as e:
        logger.error(f"Failed to list reports: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/reports/<filename>', methods=['GET'])
def download_report(filename):
    """Download a report file"""
    try:
        filepath = os.path.join(report_generator.output_dir, filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        return jsonify({'error': 'Report not found'}), 404
    except Exception as e:
        logger.error(f"Failed to download report: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ============== ROUTES - NOTIFICATIONS ==============

@app.route('/api/notifications/test', methods=['POST'])
def test_notification():
    """Send a test email notification"""
    try:
        data = request.json
        success = notifier.send_email(
            data.get('email'),
            'SmartBiz Test Email',
            'This is a test email from SmartBiz'
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Email sent'}), 200
        return jsonify({'error': 'Failed to send email'}), 500
    except Exception as e:
        logger.error(f"Failed to send test notification: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# ============== APP INITIALIZATION ==============

def init_app():
    """Initialize the application"""
    logger.info("=" * 60)
    logger.info("SmartBiz - Business Automation System")
    logger.info("=" * 60)
    
    # Check database connection
    if db.health_check():
        logger.info("✓ Database connection established")
    else:
        logger.warning("✗ Database connection failed - check credentials")
    
    # Start scheduler
    scheduler.start()
    
    logger.info("✓ Application initialized successfully")

if __name__ == '__main__':
    init_app()
    print("\n" + "="*60)
    print("🌐 SmartBiz Web Server")
    print("="*60)
    print("\n✅ Starting server...")
    print("📍 Access at: http://localhost:5000")
    print("🔴 Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
