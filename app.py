from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # 👈 ADDED
import sqlite3
import time

app = Flask(__name__)
CORS(app)  # 👈 ADDED

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            area TEXT NOT NULL,
            created_at REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            area TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at REAL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
        addr = data.get('address', '').strip()
        area = data.get('area', '').strip()
        
        if not addr or area not in {"Stanger Manor", "Oceanview"}:
            return jsonify({"error": "Invalid address or area"}), 400

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (address, area, created_at) VALUES (?, ?, ?)",
            (addr, area, time.time())
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "Registered"})
    
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/panic', methods=['POST'])
def panic():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
        addr = data.get('address', 'Anonymous')
        area = data.get('area', 'Unknown')
        
        if area not in {"Stanger Manor", "Oceanview"}:
            return jsonify({"error": "Invalid area"}), 400

        message = f"🚨 PANIC! {addr}, {area} needs help! ({time.strftime('%Y-%m-%d %H:%M:%S')})"
        
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO alerts (address, area, message, created_at) VALUES (?, ?, ?, ?)",
            (addr, area, message, time.time())
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "Alert sent to community!"})
    
    except Exception as e:
        print(f"Panic error: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/alerts')
def get_alerts():
    try:
        conn = get_db_connection()
        alerts = conn.execute(
            "SELECT message FROM alerts ORDER BY created_at DESC LIMIT 10"
        ).fetchall()
        conn.close()
        return jsonify([alert['message'] for alert in alerts])
    except Exception as e:
        print(f"Alerts fetch error: {e}")
        return jsonify([])

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)