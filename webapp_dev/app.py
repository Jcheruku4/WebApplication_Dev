from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
app = Flask(__name__)
DATABASE = 'E:/College/Web Application Development/webapp_dev/users.db'
app.secret_key = 'your_secret_key_here'
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        return render_template('sign_in.html', error="Invalid credentials. Please try again!")
    return render_template('sign_in.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('signin'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('sign_up.html', error="Username already exists. Please choose another.")
    return render_template('sign_up.html')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    return render_template('dashboard.html')
@app.route('/edit_expenditure', methods=['GET', 'POST'])
def edit_expenditure():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user_id = session['user_id']
    conn = get_db_connection()
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO expenditures (description, amount, timestamp, user_id) VALUES (?, ?, ?, ?)', 
                     (description, amount, timestamp, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('edit_expenditure'))
    filter_option = request.args.get('filter', 'all')
    order_option = request.args.get('order', 'asc')
    if filter_option == 'today':
        query = f"SELECT * FROM expenditures WHERE DATE(timestamp) = DATE('now') AND user_id = ?"
    elif filter_option == 'last_3_months':
        query = f"SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-3 months') AND user_id = ?"
    elif filter_option == 'last_6_months':
        query = f"SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-6 months') AND user_id = ?"
    elif filter_option == 'last_12_months':
        query = f"SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-12 months') AND user_id = ?"
    else:
        query = f"SELECT * FROM expenditures WHERE user_id = ?"
    if order_option == 'asc':
        query += " ORDER BY amount ASC"
    elif order_option == 'desc':
        query += " ORDER BY amount DESC"
    elif order_option == 'date_recent':
        query += " ORDER BY timestamp DESC"
    elif order_option == 'date_oldest':
        query += " ORDER BY timestamp ASC"
    expenditures = conn.execute(query, (user_id,)).fetchall()
    conn.close()
    return render_template('edit_expenditure.html', expenditures=expenditures, filter_option=filter_option, order_option=order_option)
@app.route('/delete/<int:id>', methods=['POST'])
def delete_expenditure(id):
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user_id = session['user_id']
    conn = get_db_connection()
    conn.execute('DELETE FROM expenditures WHERE id = ? AND user_id = ?', (id, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('edit_expenditure'))
@app.route('/delete_all', methods=['POST'])
def delete_all_expenditures():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user_id = session['user_id']
    conn = get_db_connection()
    conn.execute('DELETE FROM expenditures WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('edit_expenditure'))
@app.route('/expenditure_analysis', methods=['GET'])
def expenditure_analysis():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user_id = session['user_id']
    conn = get_db_connection()
    filter_option = request.args.get('filter', 'all')
    query = "SELECT * FROM expenditures WHERE user_id = ?"
    if filter_option == 'today':
        query = "SELECT * FROM expenditures WHERE DATE(timestamp) = DATE('now') AND user_id = ?"
    elif filter_option == 'last_3_months':
        query = "SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-3 months') AND user_id = ?"
    elif filter_option == 'last_6_months':
        query = "SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-6 months') AND user_id = ?"
    elif filter_option == 'last_12_months':
        query = "SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-12 months') AND user_id = ?"
    expenditures = conn.execute(query, (user_id,)).fetchall()
    conn.close()
    total_spending = sum([exp['amount'] for exp in expenditures])
    days = set([exp['timestamp'].split(' ')[0] for exp in expenditures])
    num_days = len(days)
    average_spending = total_spending / num_days if num_days > 0 else 0
    spending_by_day = {}
    for exp in expenditures:
        date = exp['timestamp'].split(' ')[0]
        spending_by_day[date] = spending_by_day.get(date, 0) + exp['amount']
    highest_day = max(spending_by_day.items(), key=lambda x: x[1], default=None)
    lowest_day = min(spending_by_day.items(), key=lambda x: x[1], default=None)
    highest_spending = sorted(expenditures, key=lambda x: x['amount'], reverse=True)[:3]
    least_spending = sorted(expenditures, key=lambda x: x['amount'])[:3]
    return render_template('expenditure_analysis.html', 
                           total_spending=total_spending,
                           average_spending=average_spending,
                           highest_spending=highest_spending,
                           least_spending=least_spending,
                           highest_day=highest_day,
                           lowest_day=lowest_day,
                           filter_option=filter_option)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))
if __name__ == '__main__':
    app.run(debug=True)
