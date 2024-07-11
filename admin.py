from flask import Blueprint, jsonify, request, session
from extensions import mysql
from utilities import write_to_csv, update_json

admin_bp = Blueprint('admin', __name__)

# Authentication decorator
def login_required(role):
    def wrapper(f):
        def wrap(*args, **kwargs):
            if 'userid' in session and session.get('role') == role:
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Unauthorized'}), 403
        wrap.__name__ = f.__name__
        return wrap
    return wrapper

# Function to convert tuple of tuples to list of dictionaries
def convert_to_dict(data):
    keys = ('id', 'employee_id', 'client_id', 'pay_date', 'No_of_hours_worked', 'overtime_hours', 'Increment')
    return [dict(zip(keys, row)) for row in data]

@admin_bp.route('/users', methods=['GET'])
@login_required('admin')
def get_users():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users')
        result = cursor.fetchall()

        write_to_csv('users', result)
        update_json('users', result)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/payrolls', methods=['POST'])
@login_required('admin')
def create_payroll():
    try:
        data = request.json
        employee_id = data.get('employee_id')
        client_id = data.get('client_id')
        pay_date = data.get('pay_date')
        No_of_hours_worked = data.get('No_of_hours_worked')
        overtime_hours = data.get('overtime_hours')
        Increment = data.get('Increment')

        if not employee_id or not client_id or not pay_date or not No_of_hours_worked or not overtime_hours or not Increment:
            return jsonify({'error': 'Please provide employee_id, client_id, pay_date, No_of_hours_worked, overtime_hours, and Increment'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO payroll (employee_id, client_id, pay_date, No_of_hours_worked, overtime_hours, Increment) VALUES (%s, %s, %s, %s, %s, %s)', (employee_id, client_id, pay_date, No_of_hours_worked, overtime_hours, Increment))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM payroll')
        result = cursor.fetchall()
        payroll_data = convert_to_dict(result)
        write_to_csv('payroll', payroll_data)
        update_json('payroll', payroll_data)

        return jsonify({'message': 'Payroll created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/payrolls', methods=['GET'])
@login_required('admin')
def get_payrolls():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM payroll')
        result = cursor.fetchall()
        payroll_data = convert_to_dict(result)

        write_to_csv('payroll', payroll_data)
        update_json('payroll', payroll_data)

        return jsonify(payroll_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/payrolls/<int:id>', methods=['GET'])
@login_required('admin')
def get_payroll(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM payroll WHERE id = %s', (id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Payroll not found'}), 404

        payroll_data = {
            'id': result[0],
            'employee_id': result[1],
            'client_id': result[2],
            'pay_date': result[3],
            'No_of_hours_worked': result[4],
            'overtime_hours': result[5],
            'Increment': result[6]
        }

        return jsonify(payroll_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/payrolls/<int:id>', methods=['PUT'])
@login_required('admin')
def update_payroll(id):
    try:
        data = request.json
        employee_id = data.get('employee_id')
        client_id = data.get('client_id')
        pay_date = data.get('pay_date')
        No_of_hours_worked = data.get('No_of_hours_worked')
        overtime_hours = data.get('overtime_hours')
        Increment = data.get('Increment')

        if not employee_id or not client_id or not pay_date or not No_of_hours_worked or not overtime_hours or not Increment:
            return jsonify({'error': 'Please provide employee_id, client_id, pay_date, No_of_hours_worked, overtime_hours, and Increment'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM payroll WHERE id = %s', (id,))
        existing_payroll = cursor.fetchone()

        if not existing_payroll:
            return jsonify({'error': 'Payroll not found'}), 404

        cursor.execute('UPDATE payroll SET employee_id = %s, client_id = %s, pay_date = %s, No_of_hours_worked = %s, overtime_hours = %s, Increment = %s WHERE id = %s', (employee_id, client_id, pay_date, No_of_hours_worked, overtime_hours, Increment, id))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM payroll')
        result = cursor.fetchall()
        payroll_data = convert_to_dict(result)
        write_to_csv('payroll', payroll_data)
        update_json('payroll', payroll_data)

        return jsonify({'message': 'Payroll updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/payrolls/<int:id>', methods=['DELETE'])
@login_required('admin')
def delete_payroll(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM payroll WHERE id = %s', (id,))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM payroll')
        result = cursor.fetchall()
        payroll_data = convert_to_dict(result)
        write_to_csv('payroll', payroll_data)
        update_json('payroll', payroll_data)

        return jsonify({'message': 'Payroll deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/calculate_payout', methods=['PUT'])
@login_required('admin')
def calculate_payout():
    try:
        payroll_id = request.json.get('payroll_id')

        if not payroll_id:
            return jsonify({'error': 'payroll_id is required'}), 400

        cursor = mysql.connection.cursor()

        # Advanced SQL query to calculate the total payout
        query = """
        SELECT
            p.id,
            p.employee_id,
            (p.No_of_hours_worked * c.hourly_pay + p.overtime_hours * c.overtime_pay + p.Increment) AS total_payout
        FROM
            payroll p
        JOIN
            clients c ON p.client_id = c.id
        WHERE
            p.id = %s
        """
        cursor.execute(query, (payroll_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Payroll record not found'}), 404

        payroll_data = {
            'id': result[0],
            'employee_id': result[1],
            'total_payout': result[2]
        }

        # Return the employee_id and total_payout as JSON
        return jsonify(payroll_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()