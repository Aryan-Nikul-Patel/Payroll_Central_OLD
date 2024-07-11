from flask import Blueprint, request, jsonify
from login import login_required
from utilities import write_to_csv, update_json
from extensions import mysql

client_bp = Blueprint('client', __name__)

# Function to convert tuple of tuples to list of dictionaries
def convert_to_dict(data):
    keys = ('id', 'name', 'contact_info', 'hourly_pay', 'overtime_pay')
    return [dict(zip(keys, row)) for row in data]

@client_bp.route('/clients', methods=['POST'])
@login_required('admin')
def create_client():
    try:
        data = request.json
        name = data.get('name')
        contact_info = data.get('contact_info')
        hourly_pay = data.get('hourly_pay')
        overtime_pay = data.get('overtime_pay')

        if not name or not contact_info or not hourly_pay or not overtime_pay:
            return jsonify({'error': 'Please provide name, contact_info, hourly_pay, and overtime_pay'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO clients (name, contact_info, hourly_pay, overtime_pay) VALUES (%s, %s, %s, %s)', (name, contact_info, hourly_pay, overtime_pay))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM clients')
        result = cursor.fetchall()
        clients_data = convert_to_dict(result)
        write_to_csv('clients', clients_data)
        update_json('clients', clients_data)

        return jsonify({'message': 'Client created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/clients', methods=['GET'])
@login_required('admin')
def get_clients():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM clients')
        result = cursor.fetchall()
        clients_data = convert_to_dict(result)

        write_to_csv('clients', clients_data)
        update_json('clients', clients_data)

        return jsonify(clients_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/clients/<int:id>', methods=['GET'])
@login_required('client')
def get_client(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM clients WHERE id = %s', (id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Client not found'}), 404

        client_data = {
            'id': result[0],
            'name': result[1],
            'contact_info': result[2],
            'hourly_pay': result[3],
            'overtime_pay': result[4]
        }

        return jsonify(client_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/clients/<int:id>', methods=['PUT'])
@login_required('admin')
def update_client(id):
    try:
        data = request.json
        name = data.get('name')
        contact_info = data.get('contact_info')
        hourly_pay = data.get('hourly_pay')
        overtime_pay = data.get('overtime_pay')

        if not name or not contact_info or not hourly_pay or not overtime_pay:
            return jsonify({'error': 'Please provide name, contact_info, hourly_pay, and overtime_pay'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM clients WHERE id = %s', (id,))
        existing_client = cursor.fetchone()

        if not existing_client:
            return jsonify({'error': 'Client not found'}), 404

        cursor.execute('UPDATE clients SET name = %s, contact_info = %s, hourly_pay = %s, overtime_pay = %s WHERE id = %s', (name, contact_info, hourly_pay, overtime_pay, id))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM clients')
        result = cursor.fetchall()
        clients_data = convert_to_dict(result)
        write_to_csv('clients', clients_data)
        update_json('clients', clients_data)

        return jsonify({'message': 'Client updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/clients/<int:id>', methods=['DELETE'])
@login_required('admin')
def delete_client(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM clients WHERE id = %s', (id,))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM clients')
        result = cursor.fetchall()
        clients_data = convert_to_dict(result)
        write_to_csv('clients', clients_data)
        update_json('clients', clients_data)

        return jsonify({'message': 'Client deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
