from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import csv
import json
import os
 
app = Flask(__name__)
 
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password@123456'
app.config['MYSQL_DB'] = 'payroll_db'
 
mysql = MySQL(app)
 
# CSV file paths
csv_files = {
    'employees': 'employees.csv',
    'clients': 'clients.csv',
    'payroll': 'payroll.csv'
}
 
# Helper functions to write to CSV
def write_to_csv(table, data):
    with open(csv_files[table], 'w', newline='') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
 
# Helper functions to read from CSV
def read_from_csv(table):
    if not os.path.exists(csv_files[table]):
        return []
    with open(csv_files[table], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
 
# Helper function to update JSON file
def update_json(table, data):
    with open(f'{table}.json', 'w') as jsonfile:
        json.dump(data, jsonfile)
 
# Employee CRUD operations
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    name = data['name']
    position = data['position']
   
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO employees (name, position) VALUES (%s, %s)', (name, position))
    mysql.connection.commit()
   
    # Update CSV and JSON
    cursor.execute('SELECT * FROM employees')
    result = cursor.fetchall()
    write_to_csv('employees', result)
    update_json('employees', result)
   
    return jsonify({'message': 'Employee created successfully'}), 201
 
@app.route('/employees', methods=['GET'])
def get_employees():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employees')
    result = cursor.fetchall()
   
    write_to_csv('employees', result)
    update_json('employees', result)
   
    return jsonify(result)
 
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employees WHERE id = %s', (id,))
    result = cursor.fetchone()
   
    if not result:
        return jsonify({'message': 'Employee not found'}), 404
   
    return jsonify(result)
 
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    name = data['name']
    position = data['position']
   
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE employees SET name = %s, position = %s WHERE id = %s', (name, position, id))
    mysql.connection.commit()
   
    cursor.execute('SELECT * FROM employees')
    result = cursor.fetchall()
    write_to_csv('employees', result)
    update_json('employees', result)
   
    return jsonify({'message': 'Employee updated successfully'})
 
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM employees WHERE id = %s', (id,))
    mysql.connection.commit()
   
    cursor.execute('SELECT * FROM employees')
    result = cursor.fetchall()
    write_to_csv('employees', result)
    update_json('employees', result)
   
    return jsonify({'message': 'Employee deleted successfully'})
 
# Client CRUD operations
@app.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    name = data['name']
    contact_info = data['contact_info']
    hourly_pay = data['hourly_pay']
    overtime_pay = data['overtime_pay']
   
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO clients (name, contact_info,hourly_pay,overtime_pay) VALUES (%s, %s, %s, %s)', (name, contact_info,hourly_pay, overtime_pay))
    mysql.connection.commit()
   
    cursor.execute('SELECT * FROM clients')
    result = cursor.fetchall()
    write_to_csv('clients', result)
    update_json('clients', result)
   
    return jsonify({'message': 'Client created successfully'}), 201
 
@app.route('/clients', methods=['GET'])
def get_clients():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM clients')
    result = cursor.fetchall()
   
    write_to_csv('clients', result)
    update_json('clients', result)
   
    return jsonify(result)
 
@app.route('/clients/<int:id>', methods=['GET'])
def get_client(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM clients WHERE id = %s', (id,))
    result = cursor.fetchone()
   
    if not result:
        return jsonify({'message': 'Client not found'}), 404
   
    return jsonify(result)
 
@app.route('/clients/<int:id>', methods=['PUT'])
def update_client(id):
    data = request.json
    name = data['name']
    contact_info = data['contact_info']
    hourly_pay = data['hourly_pay']
    overtime_pay = data['overtime_pay']
   
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE clients SET name = %s, contact_info = %s, hourly_pay = %s, overtime_pay = %s WHERE id = %s', (name, contact_info, hourly_pay,overtime_pay, id))
    mysql.connection.commit()
   
    cursor.execute('SELECT * FROM clients')
    result = cursor.fetchall()
    write_to_csv('clients', result)
    update_json('clients', result)
   
    return jsonify({'message': 'Client updated successfully'})
 
@app.route('/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM clients WHERE id = %s', (id,))
    mysql.connection.commit()
   
    cursor.execute('SELECT * FROM clients')
    result = cursor.fetchall()
    write_to_csv('clients', result)
    update_json('clients', result)
   
    return jsonify({'message': 'Client deleted successfully'})
 
# Payroll CRUD operations
@app.route('/payrolls', methods=['POST'])
def create_payroll():
    data = request.json
    employee_id = data['employee_id']
    client_id = data['client_id']
    pay_date = data['pay_date']
    No_of_hours_worked = data['No_of_hours_worked']
    overtime_hours = data['overtime_hours']
    Increment = data['Increment']
   
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO payroll (employee_id, client_id, pay_date, No_of_hours_worked,overtime_hours,Increment) VALUES (%s, %s, %s, %s, %s , %s)', (employee_id, client_id, pay_date, No_of_hours_worked,overtime_hours,Increment))
    mysql.connection.commit()
   
    cursor.execute('SELECT * FROM payroll')
    result = cursor.fetchall()
    write_to_csv('payroll', result)
    update_json('payroll', result)
   
    return jsonify({'message': 'Payroll created successfully'}), 201
 
@app.route('/payrolls', methods=['GET'])
def get_payrolls():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM payroll')
    result = cursor.fetchall()
   
    write_to_csv('payroll', result)
    update_json('payroll', result)
   
    return jsonify(result)
 
@app.route('/payrolls/<int:id>', methods=['GET'])
def get_payroll(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM payroll WHERE id = %s', (id,))
    result = cursor.fetchone()
   
    if not result:
        return jsonify({'message': 'Payroll not found'}), 404
   
    return jsonify(result)
 
@app.route('/payrolls/<int:id>', methods=['PUT'])
def update_payroll(id):
    data = request.json
    employee_id = data['employee_id']
    client_id = data['client_id']
    pay_date = data['pay_date']
    No_of_hours_worked = data['No_of_hours_worked']
    overtime_hours = data['overtime_hours']
    Increment = data['Increment']
   
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE payroll SET employee_id = %s, client_id = %s, pay_date = %s, No_of_hours_worked = %s, overtime_hours = %s, Increment = %s  WHERE id = %s', (employee_id, client_id, pay_date, No_of_hours_worked, overtime_hours, Increment , id))
    mysql.connection.commit()
   
    cursor.execute('SELECT * FROM payroll')
    result = cursor.fetchall()
    write_to_csv('payroll', result)
    update_json('payroll', result)
   
    return jsonify({'message': 'Payroll updated successfully'})
 
@app.route('/payrolls/<int:id>', methods=['DELETE'])
def delete_payroll(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM payroll WHERE id = %s', (id,))
    mysql.connection.commit()
   
    cursor.execute('SELECT * FROM payroll')
    result = cursor.fetchall()
    write_to_csv('payroll', result)
    update_json('payroll', result)
   
    return jsonify({'message': 'Payroll deleted successfully'})
 
# Additional functionalities
@app.route('/employee_payroll/<int:employee_id>', methods=['GET'])
def get_employee_payroll(employee_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM payroll WHERE employee_id = %s', (employee_id,))
    result = cursor.fetchall()
   
    if not result:
        return jsonify({'message': 'No payroll records found for this employee'}), 404
   
    return jsonify(result)
 
@app.route('/client_payroll/<int:client_id>', methods=['GET'])
def get_client_payroll(client_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM payroll WHERE client_id = %s', (client_id,))
    result = cursor.fetchall()
   
    if not result:
        return jsonify({'message': 'No payroll records found for this client'}), 404
   
    return jsonify(result)

@app.route('/')
def index():
    return "Welcome to Payroll-Management-System"

@app.route('/calculate_payout', methods=['PUT'])
def calculate_payout():
    payroll_id = request.json.get('payroll_id')

    if not payroll_id:
        return jsonify({'error': 'payroll_id is required'}), 400

    try:
        cursor = mysql.connection.cursor()

        # Advanced SQL query to calculate the total payout
        query = """
        SELECT
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

        employee_id = result[0]
        total_payout = result[1]

        # Return the emp_id and total_payout as JSON
        return jsonify({'employee_id': employee_id, 'total_payout': total_payout}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
 
