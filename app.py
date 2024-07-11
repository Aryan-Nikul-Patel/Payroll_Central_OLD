from flask import Flask
from extensions import mysql, bcrypt
from login import login_bp
from client import client_bp
from employee import employee_bp
from admin import admin_bp
from data_analytics import data_analytics_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'SQLserver@123'
    app.config['MYSQL_DB'] = 'payroll_db'

    mysql.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(login_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(admin_bp)
    # Register blueprints
    app.register_blueprint(data_analytics_bp)

    return app