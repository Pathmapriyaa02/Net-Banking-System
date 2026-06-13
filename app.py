from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import mysql.connector
import bcrypt
from datetime import datetime, timezone
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# MySQL configuration
db_config = {
    'user': 'root',
    'password': 'pathu@04',
    'host': 'localhost',
    'database': 'net_banking'
}

def set_mysql_timezone():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SET time_zone = '+00:00'")
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error setting MySQL timezone: {err}")

def check_database_schema():
    required_tables = ['users', 'transactions', 'notifications']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        for table in required_tables:
            if table not in tables:
                print(f"Error: Required table '{table}' is missing in the database.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error checking database schema: {err}")

@app.route('/')
def index():
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login and redirect based on role."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['role'] = user['role']
                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user['role'] == 'customer':
                    return redirect(url_for('payment_dashboard'))
                else:
                    flash('Unknown user role.', 'error')
                    return render_template('login.html')
            else:
                flash('Invalid email or password.', 'error')
                return render_template('login.html')
        except mysql.connector.Error as err:
            flash(f'Database error: {err}', 'error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    """Admin dashboard, only for admins."""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/payment_dashboard', methods=['GET', 'POST'])
def payment_dashboard():
    """Customer payment dashboard."""
    if 'user_id' not in session or session.get('role') != 'customer':
        flash('Access denied: Customers only.', 'error')
        return redirect(url_for('login'))

    transactions = []
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, account_type, recipient_phone, amount, transaction_date, status
            FROM transactions
            WHERE user_id = %s
            ORDER BY transaction_date DESC
        """, (session['user_id'],))
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error:
        transactions = []

    if request.method == 'POST':
        account_type = request.form.get('account_type')
        recipient_phone = request.form.get('recipient_phone')
        amount = request.form.get('amount')
        if not all([account_type, recipient_phone, amount]):
            flash('All fields are required.', 'error')
            return render_template('payment_dashboard.html', transactions=transactions)
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (user_id, account_type, recipient_phone, amount, transaction_date, status)
                VALUES (%s, %s, %s, %s, NOW(), %s)
            """, (session['user_id'], account_type, recipient_phone, amount, 'pending'))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Payment initiated successfully!', 'success')
            return redirect(url_for('payment_dashboard'))
        except mysql.connector.Error as err:
            flash(f'Database error: {err}', 'error')
            return render_template('payment_dashboard.html', transactions=transactions)

    return render_template('payment_dashboard.html', transactions=transactions)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('welcome'))

@app.route('/role_selection')
def role_selection():
    return render_template('role_selection.html')

@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    # Render a signup form or handle admin signup logic here
    return render_template('admin_signup.html')

@app.route('/customer_signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        phone = request.form.get('phone', '').strip()

        if not all([name, email, password, phone]):
            flash('All fields are required.', 'error')
            return render_template('customer_signup.html')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('Email already registered.', 'error')
                cursor.close()
                conn.close()
                return render_template('customer_signup.html')
            # Insert new customer
            cursor.execute("""
                INSERT INTO users (name, email, password, phone, role)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, hashed_password.decode('utf-8'), phone, 'customer'))
            conn.commit()
            session['user_id'] = cursor.lastrowid  # <-- Move this up!
            session['role'] = 'customer'
            cursor.close()
            conn.close()
            flash('Signup successful! You are now logged in.', 'success')
            return redirect(url_for('payment_dashboard'))
        except mysql.connector.Error as err:
            flash(f'Database error: {err}', 'error')
            return render_template('customer_signup.html')

    return render_template('customer_signup.html')

@app.route('/some_page')
def some_page():
    return render_template('some_page.html')

@app.route('/customer_dashboard')
def customer_dashboard():
    if 'user_id' not in session or session.get('role') != 'customer':
        flash('Access denied: Customers only.', 'error')
        return redirect(url_for('login'))

    user = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f'Database error: {err}', 'error')
        return redirect(url_for('login'))

    return render_template('customer_dashboard.html', user=user)

@app.route('/another_page')
def another_page():
    return render_template('another_page.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

# Initialize database checks and timezone
set_mysql_timezone()
check_database_schema()

if __name__ == '__main__':
    app.run(debug=True)
