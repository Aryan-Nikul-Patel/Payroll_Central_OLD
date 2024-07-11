from flask import Blueprint, request, jsonify
from login import login_required
from utilities import write_to_csv, update_json
from extensions import mysql

employee_bp = Blueprint('employee', __name__)

# Function to convert tuple of tuples to list of dictionaries
def convert_to_dict(data):
    keys = ('id', 'name', 'position')
    return [dict(zip(keys, row)) for row in data]

@employee_bp.route('/employees', methods=['POST'])
@login_required('admin')
def create_employee():
    try:
        data = request.json
        name = data.get('name')
        position = data.get('position')

        if not name or not position:
            return jsonify({'error': 'Please provide name and position'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO employees (name, position) VALUES (%s, %s)', (name, position))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM employees')
        result = cursor.fetchall()
        employees_data = convert_to_dict(result)
        write_to_csv('employees', employees_data)
        update_json('employees', employees_data)

        return jsonify({'message': 'Employee created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/employees', methods=['GET'])
@login_required('admin')
def get_employees():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM employees')
        result = cursor.fetchall()
        employees_data = convert_to_dict(result)

        write_to_csv('employees', employees_data)
        update_json('employees', employees_data)

        return jsonify(employees_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/employees/<int:id>', methods=['GET'])
@login_required('employee')
def get_employee(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM employees WHERE id = %s', (id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Employee not found'}), 404

        employee_data = {
            'id': result[0],
            'name': result[1],
            'position': result[2]
        }

        return jsonify(employee_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/employees/<int:id>', methods=['PUT'])
@login_required('admin')
def update_employee(id):
    try:
        data = request.json
        name = data.get('name')
        position = data.get('position')

        if not name or not position:
            return jsonify({'error': 'Please provide name and position'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM employees WHERE id = %s', (id,))
        existing_employee = cursor.fetchone()

        if not existing_employee:
            return jsonify({'error': 'Employee not found'}), 404

        cursor.execute('UPDATE employees SET name = %s, position = %s WHERE id = %s', (name, position, id))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM employees')
        result = cursor.fetchall()
        employees_data = convert_to_dict(result)
        write_to_csv('employees', employees_data)
        update_json('employees', employees_data)

        return jsonify({'message': 'Employee updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/employees/<int:id>', methods=['DELETE'])
@login_required('admin')
def delete_employee(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM employees WHERE id = %s', (id,))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM employees')
        result = cursor.fetchall()
        employees_data = convert_to_dict(result)
        write_to_csv('employees', employees_data)
        update_json('employees', employees_data)

        return jsonify({'message': 'Employee deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
