from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3
app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect('users.db')
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
            return redirect('/dashboard')
        else:
            return render_template('signin.html', error="Invalid credentials. Please try again!")
    return render_template('signin.html', error=None)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect('/')
        except sqlite3.IntegrityError:
            return render_template('signup.html', error="Username already exists. Please choose another.")
    return render_template('signup.html', error=None)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/edit_expenditure', methods=['GET', 'POST'])
def edit_expenditure():
    conn = get_db_connection()
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO expenditures (description, amount, timestamp, user_id) VALUES (?, ?, ?, ?)', 
                     (description, amount, timestamp, 1))
        conn.commit()
        conn.close()
        return redirect('/edit_expenditure')
    filter_option = request.args.get('filter', 'all')
    if filter_option == 'today':
        query = "SELECT * FROM expenditures WHERE DATE(timestamp) = DATE('now') AND user_id = ?"
    elif filter_option == 'last_3_months':
        query = "SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-3 months') AND user_id = ?"
    elif filter_option == 'last_6_months':
        query = "SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-6 months') AND user_id = ?"
    elif filter_option == 'last_12_months':
        query = "SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-12 months') AND user_id = ?"
    else:
        query = "SELECT * FROM expenditures WHERE user_id = ?"
    expenditures = conn.execute(query, (1,)).fetchall()
    conn.close()
    return render_template('edit_expenditure.html', expenditures=expenditures, filter_option=filter_option)
@app.route('/delete/<int:id>', methods=['POST'])
def delete_expenditure(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM expenditures WHERE id = ? AND user_id = ?', (id, 1))
    conn.commit()
    conn.close()
    return redirect('/edit_expenditure')
@app.route('/delete_all', methods=['POST'])
def delete_all_expenditures():
    conn = get_db_connection()
    conn.execute('DELETE FROM expenditures WHERE user_id = ?', (1,))
    conn.commit()
    conn.close()
    return redirect('/edit_expenditure')
@app.route('/expenditure_analysis', methods=['GET'])
def expenditure_analysis():
    conn = get_db_connection()
    filter_option = request.args.get('filter', 'all')
    sort_option = request.args.get('sort', 'asc')
    if filter_option == 'today':
        query = f"SELECT * FROM expenditures WHERE DATE(timestamp) = DATE('now') AND user_id = ? ORDER BY amount {sort_option}"
    elif filter_option == 'last_3_months':
        query = f"SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-3 months') AND user_id = ? ORDER BY amount {sort_option}"
    elif filter_option == 'last_6_months':
        query = f"SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-6 months') AND user_id = ? ORDER BY amount {sort_option}"
    elif filter_option == 'last_12_months':
        query = f"SELECT * FROM expenditures WHERE DATE(timestamp) >= DATE('now', '-12 months') AND user_id = ? ORDER BY amount {sort_option}"
    else:
        query = f"SELECT * FROM expenditures WHERE user_id = ? ORDER BY amount {sort_option}"
    expenditures = conn.execute(query, (1,)).fetchall()
    conn.close()
    return render_template('expenditure_analysis.html', expenditures=expenditures, filter_option=filter_option, sort_option=sort_option)
if __name__ == '__main__':
    app.run(debug=True)
