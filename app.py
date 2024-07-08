
# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mysqldb import MySQL
# import requests
# import random

# app = Flask(__name__)

# # MySQL configurations
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'SQLserver@123'
# app.config['MYSQL_DB'] = 'sk'

# mysql = MySQL(app)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     data = requests.get('https://employee-data-platform.vercel.app/api/fetchall')
#     response = data.json()
    
#     # Use MySQL cursor
#     cur = mysql.connection.cursor()

#     for i in response:
#         reg_days = random.randint(1, 30)
#         rate = random.randint(1, 30)
#         reg_pay = random.randint(1, 30)
#         overtimes = random.randint(1, 30)
#         overtimes_pay = random.randint(1, 30)
#         medical = random.randint(1, 30)
#         canteen = random.randint(1, 30)
#         house = random.randint(1, 30)
#         company_loan = random.randint(1, 30)
#         net = random.randint(1, 30)
        
#         # Check if id exists
#         cur.execute("SELECT * FROM payroll WHERE employeeID = %s", (i['id'],))
#         if cur.fetchone() is None:
#             cur.execute("INSERT INTO payroll(employeeID, Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                         (i['id'], reg_days, rate, reg_pay, overtimes, overtimes_pay, medical, canteen, house, company_loan, net))
    
#     # Commit changes
#     mysql.connection.commit()
    
#     # Fetch all payroll data
#     cur.execute("SELECT * FROM payroll")
#     result = cur.fetchall()

#     cur.close()  # Close cursor

#     if request.method == 'POST':
#         userChoice = request.form
#         choiceID = userChoice['employeeID']
#         choiceopt = userChoice['opt']
        
#         if choiceopt == 'Update':
#             return redirect(url_for('update', employeeID=choiceID))
#         elif choiceopt == 'Read':
#             return redirect(url_for('payroll'))
#         elif choiceopt == 'Create':
#             return redirect(url_for('create'))
#         elif choiceopt == 'Delete':
#             return redirect(url_for('delete', employeeID=choiceID))
#         return redirect(url_for('payroll'))

#     return render_template('index.html', payrollDetails=result)

# @app.route('/create', methods=['GET', 'POST'])
# def create():
#     # Use MySQL cursor
#     cur = mysql.connection.cursor()

#     if request.method == 'POST':
#         userDetails = request.form
#         employeeID = userDetails['employeeID']
#         Regular_days = userDetails['Regular_days']
#         Rate = userDetails['Rate']
#         Regular_pay = userDetails['Regular_pay']
#         Overtimes = userDetails['Overtimes']
#         Overtimes_pay = userDetails['Overtimes_pay']
#         medical = userDetails['medical']
#         canteen = userDetails['canteen']
#         house = userDetails['house']
#         company_loan = userDetails['company_loan']
#         NET = userDetails['NET']
        
#         cur.execute("INSERT INTO payroll(employeeID, Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                     (employeeID, Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET))
        
#         # Commit changes
#         mysql.connection.commit()
        
#         cur.close()  # Close cursor

#         return redirect(url_for('payroll'))

#     return render_template('create.html')

# @app.route('/payroll')
# def payroll():
#     # Use MySQL cursor
#     cur = mysql.connection.cursor()

#     cur.execute("SELECT * FROM payroll")
#     res = cur.fetchall()

#     cur.close()  # Close cursor

#     if len(res) > 0:
#         return render_template('payroll.html', payrollDetails=res)
#     else:
#         return render_template('payroll.html', payrollDetails=None)

# @app.route('/update/<string:employeeID>', methods=['GET', 'POST'])
# def update(employeeID):
#     # Use MySQL cursor
#     cur = mysql.connection.cursor()

#     cur.execute("SELECT * FROM payroll WHERE employeeID = %s", (employeeID,))
#     res = cur.fetchall()
    
#     if len(res) > 0:
#         result = res[0]  # Assuming only one record will match
        
#     if request.method == 'POST':
#         userDetails = request.form
#         employeeID = userDetails['employeeID']
#         Regular_days = userDetails['Regular_days']
#         Rate = userDetails['Rate']
#         Regular_pay = userDetails['Regular_pay']
#         Overtimes = userDetails['Overtimes']
#         Overtimes_pay = userDetails['Overtimes_pay']
#         medical = userDetails['medical']
#         canteen = userDetails['canteen']
#         house = userDetails['house']
#         company_loan = userDetails['company_loan']
#         NET = userDetails['NET']
        
#         cur.execute("UPDATE payroll SET Regular_days = %s, Rate = %s, Regular_pay = %s, Overtimes = %s, Overtimes_pay = %s, medical = %s, canteen = %s, house = %s, company_loan = %s, NET = %s WHERE employeeID = %s",
#                     (Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET, employeeID))
        
#         # Commit changes
#         mysql.connection.commit()
        
#         flash("Employee Updated Successfully")

#         cur.execute("SELECT * FROM payroll WHERE employeeID = %s", (employeeID,))
#         res = cur.fetchall()
#         if len(res) > 0:
#             result = res[0]  # Update result after update
        
#         cur.close()  # Close cursor

#     return render_template('update.html', payrollDetails=result)

# @app.route('/delete/<string:employeeID>', methods=['GET'])
# def delete(employeeID):
#     # Use MySQL cursor
#     cur = mysql.connection.cursor()

#     cur.execute("DELETE FROM payroll WHERE employeeID = %s", (employeeID,))
    
#     # Commit changes
#     mysql.connection.commit()
    
#     flash("Employee Deleted Successfully")

#     cur.close()  # Close cursor

#     return redirect(url_for('payroll'))

# if __name__ == '__main__':
#     # Set the secret key to some random bytes. Keep this really secret!
#     app.secret_key = 'super secret key'
#     # Set the session cookie to be secure
#     app.config['SESSION_TYPE'] = 'filesystem'
#     # Set the debug flag to true
#     app.debug = True
#     # Run the app :)
#     app.run()




# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mysqldb import MySQL
# import requests
# import random

# app = Flask(__name__)

# # MySQL configurations
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'SQLserver@123'
# app.config['MYSQL_DB'] = 'sk'  # Replace with your actual database name

# mysql = MySQL(app)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         userChoice = request.form
#         choiceID = userChoice['employeeID']
#         choiceopt = userChoice['opt']
        
#         if choiceopt == 'Update':
#             return redirect(url_for('update', employeeID=choiceID))
#         elif choiceopt == 'Read':
#             return redirect(url_for('payroll'))
#         elif choiceopt == 'Create':
#             return redirect(url_for('create'))
#         elif choiceopt == 'Delete':
#             return redirect(url_for('delete', employeeID=choiceID))
#         return redirect(url_for('payroll'))

#     # Fetch all payroll data
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM payroll")
#     result = cur.fetchall()
#     cur.close()  # Close cursor

#     return render_template('index.html', payrollDetails=result)

# @app.route('/create', methods=['GET', 'POST'])
# def create():
#     if request.method == 'POST':
#         userDetails = request.form
#         employeeID = userDetails['employeeID']
#         Regular_days = int(userDetails['Regular_days'])  # Convert to int as needed
#         Rate = int(userDetails['Rate'])
#         Regular_pay = int(userDetails['Regular_pay'])
#         Overtimes = int(userDetails['Overtimes'])
#         Overtimes_pay = int(userDetails['Overtimes_pay'])
#         medical = int(userDetails['medical'])
#         canteen = int(userDetails['canteen'])
#         house = int(userDetails['house'])
#         company_loan = int(userDetails['company_loan'])
#         NET = int(userDetails['NET'])
        
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO payroll(employeeID, Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                     (employeeID, Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET))
#         mysql.connection.commit()
#         cur.close()

#         return redirect(url_for('payroll'))

#     return render_template('create.html')

# @app.route('/payroll')
# def payroll():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM payroll")
#     res = cur.fetchall()
#     cur.close()

#     return render_template('payroll.html', payrollDetails=res)

# @app.route('/update/<int:employeeID>', methods=['PUT'])
# def update(employeeID):
#     print("sasi")
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM payroll WHERE employeeID = %s", (employeeID,))
#     res = cur.fetchone()
    
#     if res:
#         if request.method == 'PUT':
#             userDetails = request.form
#             Regular_days = int(userDetails['Regular_days'])
#             Rate = int(userDetails['Rate'])
#             Regular_pay = int(userDetails['Regular_pay'])
#             Overtimes = int(userDetails['Overtimes'])
#             Overtimes_pay = int(userDetails['Overtimes_pay'])
#             medical = int(userDetails['medical'])
#             canteen = int(userDetails['canteen'])
#             house = int(userDetails['house'])
#             company_loan = int(userDetails['company_loan'])
#             NET = int(userDetails['NET'])
            
#             cur.execute("UPDATE payroll SET Regular_days = %s, Rate = %s, Regular_pay = %s, Overtimes = %s, Overtimes_pay = %s, medical = %s, canteen = %s, house = %s, company_loan = %s, NET = %s WHERE employeeID = %s",
#                         (Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET, employeeID))
#             mysql.connection.commit()
#             cur.close()

#             flash("Employee Updated Successfully")
#             return redirect(url_for('payroll'))

#         cur.close()
#         return render_template('update.html', payrollDetails=res)

#     else:
#         cur.close()
#         return 'Employee not found', 404

# @app.route('/delete/<string:employeeID>', methods=['GET'])
# def delete(employeeID):
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM payroll WHERE employeeID = %s", (employeeID,))
#     mysql.connection.commit()
#     cur.close()

#     flash("Employee Deleted Successfully")
#     return redirect(url_for('payroll'))

# if __name__ == '__main__':
#     app.secret_key = 'super secret key'
#     app.run(debug=True)



# from flask import Flask, request, jsonify
# from flask_mysqldb import MySQL
# from flask import jsonify

# app = Flask(__name__)

# # MySQL configurations
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'SQLserver@123'
# app.config['MYSQL_DB'] = 'sk'  # Replace with your actual database name

# mysql = MySQL(app)

# # Endpoint to handle CRUD operations

# @app.route('/payroll', methods=['GET', 'POST'])
# def handle_payroll():
#     if request.method == 'GET':
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM payroll")
#         res = cur.fetchall()
#         cur.close()
        
#         payroll_list = []
#         for payroll in res:
#             payroll_dict = {
#                 'employeeID': payroll[0],
#                 'Regular_days': payroll[1],
#                 'Rate': payroll[2],
#                 'Regular_pay': payroll[3],
#                 'Overtimes': payroll[4],
#                 'Overtimes_pay': payroll[5],
#                 'medical': payroll[6],
#                 'canteen': payroll[7],
#                 'house': payroll[8],
#                 'company_loan': payroll[9],
#                 'NET': payroll[10]
#             }
#             payroll_list.append(payroll_dict)
        
#         return jsonify(payroll_list)

#     elif request.method == 'POST':
#         userDetails = request.json
#         employeeID = userDetails['employeeID']
#         Regular_days = userDetails['Regular_days']
#         Rate = userDetails['Rate']
#         Regular_pay = userDetails['Regular_pay']
#         Overtimes = userDetails['Overtimes']
#         Overtimes_pay = userDetails['Overtimes_pay']
#         medical = userDetails['medical']
#         canteen = userDetails['canteen']
#         house = userDetails['house']
#         company_loan = userDetails['company_loan']
#         NET = userDetails['NET']
        
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO payroll(employeeID, Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                     (employeeID, Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET))
#         mysql.connection.commit()
#         cur.close()

#         return jsonify({"message": "Payroll entry created successfully"})

# @app.route('/payroll/<int:employeeID>', methods=['GET', 'PUT', 'DELETE'])
# def handle_single_payroll(employeeID):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM payroll WHERE employeeID = %s", (employeeID,))
#     res = cur.fetchone()
    
#     if not res:
#         return jsonify({"error": "Employee not found"}), 404
    
#     if request.method == 'GET':
#         payroll_dict = {
#             'employeeID': res[0],
#             'Regular_days': res[1],
#             'Rate': res[2],
#             'Regular_pay': res[3],
#             'Overtimes': res[4],
#             'Overtimes_pay': res[5],
#             'medical': res[6],
#             'canteen': res[7],
#             'house': res[8],
#             'company_loan': res[9],
#             'NET': res[10]
#         }
#         cur.close()
#         return jsonify(payroll_dict)
    
#     elif request.method == 'PUT':
#         userDetails = request.json
#         Regular_days = userDetails['Regular_days']
#         Rate = userDetails['Rate']
#         Regular_pay = userDetails['Regular_pay']
#         Overtimes = userDetails['Overtimes']
#         Overtimes_pay = userDetails['Overtimes_pay']
#         medical = userDetails['medical']
#         canteen = userDetails['canteen']
#         house = userDetails['house']
#         company_loan = userDetails['company_loan']
#         NET = userDetails['NET']
        
#         cur.execute("UPDATE payroll SET Regular_days = %s, Rate = %s, Regular_pay = %s, Overtimes = %s, Overtimes_pay = %s, medical = %s, canteen = %s, house = %s, company_loan = %s, NET = %s WHERE employeeID = %s",
#                     (Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET, employeeID))
#         mysql.connection.commit()
#         cur.close()

#         return jsonify({"message": "Payroll entry updated successfully"})

#     elif request.method == 'DELETE':
#         cur.execute("DELETE FROM payroll WHERE employeeID = %s", (employeeID,))
#         mysql.connection.commit()
#         cur.close()

#         return jsonify({"message": "Payroll entry deleted successfully"})

# if __name__ == '__main__':
#     app.run(debug=True)


# import io
# import csv
# from flask import Flask, request, jsonify, Response, make_response
# from flask_mysqldb import MySQL

# app = Flask(__name__)

# # MySQL configurations
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'SQLserver@123'
# app.config['MYSQL_DB'] = 'sk'  # Replace with your actual database name

# mysql = MySQL(app)

# @app.route('/payroll/create', methods=['POST'])
# def create_payroll():
#     userDetails = request.json
#     # Extract details from JSON
#     # Ensure to validate and sanitize input data before querying
#     cur = mysql.connection.cursor()
#     cur.execute("INSERT INTO payroll(employeeID, Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                 (userDetails['employeeID'], userDetails['Regular_days'], userDetails['Rate'], userDetails['Regular_pay'], userDetails['Overtimes'], userDetails['Overtimes_pay'], userDetails['medical'], userDetails['canteen'], userDetails['house'], userDetails['company_loan'], userDetails['NET']))
#     mysql.connection.commit()
#     cur.close()

#     return jsonify({"message": "Payroll entry created successfully"})
# @app.route('/payroll', methods=['GET'])
# def read_all_payrolls():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM payroll")
#     res = cur.fetchall()
#     cur.close()

#     payroll_list = []
#     for payroll in res:
#         payroll_dict = {
#             'employeeID': payroll[0],
#             'Regular_days': payroll[1],
#             'Rate': payroll[2],
#             'Regular_pay': payroll[3],
#             'Overtimes': payroll[4],
#             'Overtimes_pay': payroll[5],
#             'medical': payroll[6],
#             'canteen': payroll[7],
#             'house': payroll[8],
#             'company_loan': payroll[9],
#             'NET': payroll[10]
#         }
#         payroll_list.append(payroll_dict)

#     return jsonify(payroll_list)
# @app.route('/payroll/<int:employeeID>', methods=['GET'])
# def read_single_payroll(employeeID):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM payroll WHERE employeeID = %s", (employeeID,))
#     res = cur.fetchone()
#     cur.close()

#     if res:
#         payroll_dict = {
#             'employeeID': res[0],
#             'Regular_days': res[1],
#             'Rate': res[2],
#             'Regular_pay': res[3],
#             'Overtimes': res[4],
#             'Overtimes_pay': res[5],
#             'medical': res[6],
#             'canteen': res[7],
#             'house': res[8],
#             'company_loan': res[9],
#             'NET': res[10]
#         }
#         return jsonify(payroll_dict)
#     else:
#         return jsonify({"error": "Employee not found"}), 404
# @app.route('/payroll/update/<int:employeeID>', methods=['PUT'])
# def update_payroll(employeeID):
#     userDetails = request.json
#     cur = mysql.connection.cursor()
#     cur.execute("UPDATE payroll SET Regular_days = %s, Rate = %s, Regular_pay = %s, Overtimes = %s, Overtimes_pay = %s, medical = %s, canteen = %s, house = %s, company_loan = %s, NET = %s WHERE employeeID = %s",
#                 (userDetails['Regular_days'], userDetails['Rate'], userDetails['Regular_pay'], userDetails['Overtimes'], userDetails['Overtimes_pay'], userDetails['medical'], userDetails['canteen'], userDetails['house'], userDetails['company_loan'], userDetails['NET'], employeeID))
#     mysql.connection.commit()
#     cur.close()

#     return jsonify({"message": "Payroll entry updated successfully"})

# @app.route('/payroll/delete/<int:employeeID>', methods=['DELETE'])
# def delete_payroll(employeeID):
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM payroll WHERE employeeID = %s", (employeeID,))
#     mysql.connection.commit()
#     cur.close()

#     return jsonify({"message": "Payroll entry deleted successfully"})


# # Route to export payroll data as CSV file
# @app.route('/payroll/export/csv', methods=['GET'])
# def export_payroll_csv():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM payroll")
#     res = cur.fetchall()
#     cur.close()

#     # Generate CSV data
#     output = io.StringIO()
#     writer = csv.writer(output)

#     # Write header
#     writer.writerow(['employeeID', 'Regular_days', 'Rate', 'Regular_pay', 'Overtimes', 'Overtimes_pay', 'medical', 'canteen', 'house', 'company_loan', 'NET'])

#     # Write rows
#     for payroll in res:
#         writer.writerow(payroll)

#     # Save CSV data to a file
#     csv_data = output.getvalue()
#     with open('payroll_export.csv', 'w', newline='') as f:
#         f.write(csv_data)

#     # Create response to download the file
#     response = make_response(csv_data)
#     response.headers['Content-Type'] = 'text/csv'
#     response.headers['Content-Disposition'] = 'attachment; filename=payroll_export.csv'

#     return response

# if __name__ == '__main__':
#     app.run(debug=True)


import io
import csv
from flask import Flask, request, jsonify, Response, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SQLserver@123'
app.config['MYSQL_DB'] = 'sk'  # Replace with your actual database name

mysql = MySQL(app)

# Function to export payroll data to CSV
def export_payroll_to_csv():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM payroll")
    res = cur.fetchall()
    cur.close()

    # Generate CSV data
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['employeeID', 'Regular_days', 'Rate', 'Regular_pay', 'Overtimes', 'Overtimes_pay', 'medical', 'canteen', 'house', 'company_loan', 'NET'])

    # Write rows
    for payroll in res:
        writer.writerow(payroll)

    # Save CSV data to a file
    csv_data = output.getvalue()
    with open('payroll_export.csv', 'w', newline='') as f:
        f.write(csv_data)

# Route to create a new payroll entry
@app.route('/payroll/create', methods=['POST'])
def create_payroll():
    userDetails = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO payroll(employeeID, Regular_days, Rate, Regular_pay, Overtimes, Overtimes_pay, medical, canteen, house, company_loan, NET) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (userDetails['employeeID'], userDetails['Regular_days'], userDetails['Rate'], userDetails['Regular_pay'], userDetails['Overtimes'], userDetails['Overtimes_pay'], userDetails['medical'], userDetails['canteen'], userDetails['house'], userDetails['company_loan'], userDetails['NET']))
    mysql.connection.commit()
    cur.close()

    # Export updated payroll data to CSV after creating entry
    export_payroll_to_csv()

    return jsonify({"message": "Payroll entry created successfully"})

# Route to update an existing payroll entry
@app.route('/payroll/update/<int:employeeID>', methods=['PUT'])
def update_payroll(employeeID):
    userDetails = request.json
    cur = mysql.connection.cursor()
    cur.execute("UPDATE payroll SET Regular_days = %s, Rate = %s, Regular_pay = %s, Overtimes = %s, Overtimes_pay = %s, medical = %s, canteen = %s, house = %s, company_loan = %s, NET = %s WHERE employeeID = %s",
                (userDetails['Regular_days'], userDetails['Rate'], userDetails['Regular_pay'], userDetails['Overtimes'], userDetails['Overtimes_pay'], userDetails['medical'], userDetails['canteen'], userDetails['house'], userDetails['company_loan'], userDetails['NET'], employeeID))
    mysql.connection.commit()
    cur.close()

    # Export updated payroll data to CSV after updating entry
    export_payroll_to_csv()

    return jsonify({"message": "Payroll entry updated successfully"})

# Route to delete a payroll entry
@app.route('/payroll/delete/<int:employeeID>', methods=['DELETE'])
def delete_payroll(employeeID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM payroll WHERE employeeID = %s", (employeeID,))
    mysql.connection.commit()
    cur.close()

    # Export updated payroll data to CSV after deleting entry
    export_payroll_to_csv()

    return jsonify({"message": "Payroll entry deleted successfully"})

# Route to retrieve all payroll entries
@app.route('/payroll', methods=['GET'])
def read_all_payrolls():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM payroll")
    res = cur.fetchall()
    cur.close()

    payroll_list = []
    for payroll in res:
        payroll_dict = {
            'employeeID': payroll[0],
            'Regular_days': payroll[1],
            'Rate': payroll[2],
            'Regular_pay': payroll[3],
            'Overtimes': payroll[4],
            'Overtimes_pay': payroll[5],
            'medical': payroll[6],
            'canteen': payroll[7],
            'house': payroll[8],
            'company_loan': payroll[9],
            'NET': payroll[10]
        }
        payroll_list.append(payroll_dict)

    return jsonify(payroll_list)

# Route to retrieve details of a specific payroll entry by employeeID
@app.route('/payroll/<int:employeeID>', methods=['GET'])
def read_payroll(employeeID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM payroll WHERE employeeID = %s", (employeeID,))
    payroll = cur.fetchone()
    cur.close()

    if not payroll:
        return jsonify({"message": "Payroll entry not found"}), 404

    payroll_dict = {
        'employeeID': payroll[0],
        'Regular_days': payroll[1],
        'Rate': payroll[2],
        'Regular_pay': payroll[3],
        'Overtimes': payroll[4],
        'Overtimes_pay': payroll[5],
        'medical': payroll[6],
        'canteen': payroll[7],
        'house': payroll[8],
        'company_loan': payroll[9],
        'NET': payroll[10]
    }

    return jsonify(payroll_dict)



# Route to export payroll data as CSV file
@app.route('/payroll/export/csv', methods=['GET'])
def export_payroll_csv():
    # Call the export function directly to ensure latest data
    export_payroll_to_csv()

    # Read the CSV file and serve as a response
    with open('payroll_export.csv', 'r') as f:
        csv_data = f.read()

    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=payroll_export.csv'

    return response

if __name__ == '__main__':
    app.run(debug=True)
