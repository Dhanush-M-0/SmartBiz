"""
Employees API Endpoints
GET    /api/employees         - List all employees
POST   /api/employees         - Create employee
GET    /api/employees/:id     - Get one employee
PUT    /api/employees/:id     - Update employee
DELETE /api/employees/:id     - Delete employee
"""

from flask import Blueprint, request, jsonify
from .. import models

bp = Blueprint('employees', __name__, url_prefix='/api/employees')


@bp.route('', methods=['GET'])
def get_all():
    """List all employees"""
    try:
        employees = models.get_all_employees()
        return jsonify({"success": True, "data": employees}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route('/<emp_id>', methods=['GET'])
def get_one(emp_id):
    """Get one employee by ID"""
    try:
        employee = models.get_employee_by_id(emp_id)
        if not employee:
            return jsonify({"success": False, "error": "Employee not found"}), 404
        return jsonify({"success": True, "data": employee}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route('', methods=['POST'])
def create():
    """Create new employee"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('department'):
            return jsonify({
                "success": False,
                "error": "Missing required fields: name, email, department"
            }), 400
        
        # Create employee
        employee = models.add_employee(
            name=data['name'],
            email=data['email'],
            department=data['department']
        )
        
        return jsonify({
            "success": True,
            "data": employee,
            "message": "Employee created successfully"
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route('/<emp_id>', methods=['PUT'])
def update(emp_id):
    """Update employee"""
    try:
        data = request.get_json()
        
        # For now, fetch and update all fields
        # In production, only update provided fields
        name = data.get('name')
        email = data.get('email')
        department = data.get('department')
        
        if not name or not email or not department:
            return jsonify({
                "success": False,
                "error": "Missing required fields: name, email, department"
            }), 400
        
        # Delete old and create new (since Supabase client doesn't have direct update via ID easily)
        # Better approach: use Supabase client directly
        from ..database import get_client
        result = get_client().table('employees').update({
            'name': name,
            'email': email,
            'department': department
        }).eq('id', emp_id).execute()
        
        return jsonify({
            "success": True,
            "data": result.data,
            "message": "Employee updated successfully"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route('/<emp_id>', methods=['DELETE'])
def delete(emp_id):
    """Delete employee"""
    try:
        models.delete_employee(emp_id)
        return jsonify({
            "success": True,
            "message": "Employee deleted successfully"
        }), 204
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
