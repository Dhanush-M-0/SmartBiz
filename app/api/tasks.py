"""
Tasks API Endpoints
GET    /api/tasks             - List all tasks
POST   /api/tasks             - Create task
GET    /api/tasks/:id         - Get one task
PUT    /api/tasks/:id         - Update task
DELETE /api/tasks/:id         - Delete task
"""

from flask import Blueprint, request, jsonify
from .. import models

bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@bp.route('', methods=['GET'])
def get_all():
    """List all tasks with optional status filter"""
    try:
        status = request.args.get('status')
        
        if status:
            tasks = models.get_tasks_by_status(status)
        else:
            tasks = models.get_all_tasks()
        
        # Transform due_date to deadline for frontend compatibility
        for task in tasks:
            if 'due_date' in task:
                task['deadline'] = task['due_date']
            # Capitalize status for frontend display
            if 'status' in task and task['status']:
                task['status'] = task['status'].title()
            if 'priority' in task and task['priority']:
                task['priority'] = task['priority'].title()
        
        return jsonify({"success": True, "data": tasks}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route('/<task_id>', methods=['GET'])
def get_one(task_id):
    """Get one task by ID"""
    try:
        from ..database import get_client
        result = get_client().table('tasks').select(
            '*, employees(name, email, department)'
        ).eq('id', task_id).single().execute()
        
        if not result.data:
            return jsonify({"success": False, "error": "Task not found"}), 404
        return jsonify({"success": True, "data": result.data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route('', methods=['POST'])
def create():
    """Create new task"""
    try:
        data = request.get_json()
        
        # Validate required fields (only title is truly required)
        if not data.get('title'):
            return jsonify({
                "success": False,
                "error": "Missing required field: title"
            }), 400
        
        # Create task
        task = models.add_task(
            title=data['title'],
            description=data.get('description', ''),
            assigned_to=data.get('assigned_to'),
            priority=data.get('priority', 'Medium'),
            deadline=data.get('deadline')  # Optional
        )
        
        return jsonify({
            "success": True,
            "data": task,
            "message": "Task created successfully"
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route('/<task_id>', methods=['PUT'])
def update(task_id):
    """Update task"""
    try:
        data = request.get_json()
        
        # Allow partial updates
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'status' in data:
            # Convert to lowercase for Supabase check constraint
            update_data['status'] = data['status'].lower() if data['status'] else data['status']
        if 'priority' in data:
            # Convert to lowercase for Supabase check constraint
            update_data['priority'] = data['priority'].lower() if data['priority'] else data['priority']
        if 'deadline' in data:
            update_data['due_date'] = data['deadline']
        if 'assigned_to' in data:
            update_data['assigned_to'] = data['assigned_to']
        
        if not update_data:
            return jsonify({
                "success": False,
                "error": "No fields to update"
            }), 400
        
        from ..database import get_client
        result = get_client().table('tasks').update(update_data).eq('id', task_id).execute()
        
        return jsonify({
            "success": True,
            "data": result.data,
            "message": "Task updated successfully"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route('/<task_id>', methods=['DELETE'])
def delete(task_id):
    """Delete task"""
    try:
        models.delete_task(task_id)
        return jsonify({
            "success": True,
            "message": "Task deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
