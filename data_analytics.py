from flask import Blueprint, send_file, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

data_analytics_bp = Blueprint('data_analytics', __name__)

csv_folder = os.path.dirname(__file__)

csv_files = {
    'employees': os.path.join(csv_folder, 'employees.csv'),
    'clients': os.path.join(csv_folder, 'clients.csv'),
    'payroll': os.path.join(csv_folder, 'payroll.csv'),
    'TotalSalary': os.path.join(csv_folder, 'TotalSalary.csv'),
    'users': os.path.join(csv_folder, 'users.csv')
}

# Ensure seaborn is set up
sns.set(style="whitegrid")

def save_and_return_plot(fig, filename):
    fig.savefig(filename)
    plt.close(fig)
    return send_file(filename, mimetype='image/png')

@data_analytics_bp.route('/hours_vs_payout', methods=['GET'])
def hours_vs_payout():
    payroll_df = pd.read_csv(csv_files['payroll'])
    total_salary_df = pd.read_csv(csv_files['TotalSalary'])
    merged_df = payroll_df.merge(total_salary_df, left_on='employee_id', right_on='employee_id')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=merged_df['No_of_hours_worked'], y=merged_df['total_payout'], ax=ax)
    ax.set_title('Hours Worked vs. Total Payout')
    ax.set_xlabel('Hours Worked')
    ax.set_ylabel('Total Payout')

    return save_and_return_plot(fig, 'hours_vs_payout.png')

@data_analytics_bp.route('/hourly_pay_distribution', methods=['GET'])
def hourly_pay_distribution():
    clients_df = pd.read_csv(csv_files['clients'])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(clients_df['hourly_pay'], bins=20, kde=True, ax=ax)
    ax.set_title('Distribution of Hourly Pay')
    ax.set_xlabel('Hourly Pay')
    ax.set_ylabel('Frequency')

    return save_and_return_plot(fig, 'hourly_pay_distribution.png')

@data_analytics_bp.route('/employees_by_position', methods=['GET'])
def employees_by_position():
    employees_df = pd.read_csv(csv_files['employees'])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=employees_df, x='position', ax=ax)
    ax.set_title('Number of Employees by Position')
    ax.set_xlabel('Position')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)

    return save_and_return_plot(fig, 'employees_by_position.png')

@data_analytics_bp.route('/payout_by_position', methods=['GET'])
def payout_by_position():
    payroll_df = pd.read_csv(csv_files['payroll'])
    total_salary_df = pd.read_csv(csv_files['TotalSalary'])
    employees_df = pd.read_csv(csv_files['employees'])
    merged_df = payroll_df.merge(total_salary_df, left_on='employee_id', right_on='employee_id')
    merged_df = merged_df.merge(employees_df, left_on='employee_id', right_on='id')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=merged_df, x='position', y='total_payout', ax=ax)
    ax.set_title('Total Payout by Position')
    ax.set_xlabel('Position')
    ax.set_ylabel('Total Payout')
    plt.xticks(rotation=45)

    return save_and_return_plot(fig, 'payout_by_position.png')