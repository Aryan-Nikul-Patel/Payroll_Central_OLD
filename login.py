from flask import Blueprint, request, jsonify, session, redirect, url_for
from functools import wraps
from extensions import mysql, bcrypt
from utilities import write_to_csv, update_json

login_bp = Blueprint('login', __name__)

# User registration
@login_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        userid = data.get('userid')
        password = data.get('password')
        role = data.get('role')

        if not userid or not password or not role:
            return jsonify({'error': 'Please provide userid, password, and role'}), 400

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (userid, password_hash, role) VALUES (%s, %s, %s)', (userid, password_hash, role))
        mysql.connection.commit()

        cursor.execute('SELECT * FROM users')
        users_data = cursor.fetchall()

        # Convert tuple of tuples to list of dictionaries
        users_data = [{'userid': row[0], 'password_hash': row[1], 'role': row[2]} for row in users_data]

        # Update users.csv and users.json
        write_to_csv('users', users_data)
        update_json('users', users_data)

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# User login
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        userid = data.get('userid')
        password = data.get('password')

        if not userid or not password:
            return jsonify({'error': 'Please provide userid and password'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE userid = %s', (userid,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[2], password):  # Assuming 'password_hash' is at index 2
            session['userid'] = user[0]  # Assuming 'userid' is at index 0
            session['role'] = user[3]  # Assuming 'role' is at index 3
            return jsonify({'message': 'Login successful', 'role': user[3]}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Logout route
@login_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


# Authentication decorator
def login_required(role):
    def wrapper(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'userid' in session and session.get('role') == role:
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Unauthorized'}), 403
        return wrap
    return wrapper
