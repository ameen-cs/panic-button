from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
import time
import requests

app = Flask(__name__)
CORS(app)

# 🔑 YOUR SUPABASE CREDENTIALS (from your message)
SUPABASE_URL = "https://vgyhzumjabtwzosghajo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZneWh6dW1qYWJ0d3pvc2doYWpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA5OTMzMzAsImV4cCI6MjA3NjU2OTMzMH0.eoJju7K2-ACR5X5WhPQZW3qcGPS9NlDOks3ZiB9nTSU"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def index():
    return render_template('index.html')

def supabase_insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    response = requests.post(url, json=data, headers=HEADERS)
    return response

def supabase_select(table, order="created_at", limit=10):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select=message&order={order}.desc&limit={limit}"
    response = requests.get(url, headers=HEADERS)
    return response

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

        res = supabase_insert("users", {
            "address": addr,
            "area": area,
            "created_at": time.time()
        })
        if res.status_code != 201:
            print("Supabase error (users):", res.status_code, res.text)
            return jsonify({"error": "Failed to register"}), 500

        return jsonify({"status": "Registered"})
    
    except Exception as e:
        print("Registration exception:", e)
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
        
        res = supabase_insert("alerts", {
            "address": addr,
            "area": area,
            "message": message,
            "created_at": time.time()
        })
        if res.status_code != 201:
            print("Supabase error (alerts):", res.status_code, res.text)
            return jsonify({"error": "Failed to send alert"}), 500

        return jsonify({"status": "Alert sent to community!"})
    
    except Exception as e:
        print("Panic exception:", e)
        return jsonify({"error": "Server error"}), 500

@app.route('/alerts')
def get_alerts():
    try:
        res = supabase_select("alerts")
        if res.status_code == 200:
            data = res.json()
            return jsonify([item['message'] for item in data])
        else:
            print("Alerts fetch error:", res.status_code, res.text)
            return jsonify([])
    except Exception as e:
        print("Alerts exception:", e)
        return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)), debug=True)