from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import threading
import sqlite3
import os
import sys
if sys.platform.startswith('win'):
    import sensor_monitor_mock as sensor_monitor
else:
    import sensor_monitor_real as sensor_monitor

app = Flask(__name__)
app.secret_key = '78923492jhfjhisniu2uie29'  # cần cho flash message

DB_PATH = 'database.db'

# --- Database helper ---
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE receivers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()
        conn.close()

def get_receivers():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, email FROM receivers ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def add_receiver(name, email):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO receivers (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def delete_receiver(receiver_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM receivers WHERE id = ?', (receiver_id,))
    conn.commit()
    conn.close()

# --- Start sensor monitoring thread ---
def sensor_thread():
    sensor_monitor.monitor_sensors()

threading.Thread(target=sensor_thread, daemon=True).start()

# --- Routes ---
@app.route('/')
def index():
    status, logs = sensor_monitor.get_status()
    return render_template('index.html', status=status, logs=logs)

@app.route('/api/status')
def api_status():
    status, logs = sensor_monitor.get_status()
    return jsonify(status=status, logs=logs)

# Quản lý người nhận cảnh báo
@app.route('/receivers')
def receivers():
    receivers_list = get_receivers()
    return render_template('receivers.html', receivers=receivers_list)

@app.route('/receivers/add', methods=['POST'])
def add_receiver_route():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    if not name or not email:
        flash('Tên và email không được để trống.', 'danger')
        return redirect(url_for('receivers'))
    success = add_receiver(name, email)
    if success:
        flash('Thêm người nhận cảnh báo thành công.', 'success')
    else:
        flash('Email đã tồn tại.', 'warning')
    return redirect(url_for('receivers'))

@app.route('/receivers/delete/<int:receiver_id>', methods=['POST'])
def delete_receiver_route(receiver_id):
    delete_receiver(receiver_id)
    flash('Xóa người nhận cảnh báo thành công.', 'success')
    return redirect(url_for('receivers'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
