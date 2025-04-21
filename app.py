# app.py (corregido)
import os
import sqlite3
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Conexión segura a la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>')
def user_profile(username):
    conn = get_db_connection()
    # Corregido: Usar consulta parametrizada
    query = "SELECT * FROM users WHERE username = ?"
    user = conn.execute(query, (username,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    return jsonify({"error": "User not found"}), 404

@app.route('/run_command')
def run_command():
    command = request.args.get('cmd', '')
    # Corregido: Usar subprocess con lista de argumentos
    result = subprocess.run(["echo", command], capture_output=True, text=True, check=True)
    return jsonify({"result": result.stdout})

@app.route('/config')
def get_config():
    # Corregido: Usar variables de entorno
    api_key = os.environ.get("API_KEY", "default_key_for_development")
    # Corregido: Usar dirección de enlace configurable
    bind_address = os.environ.get("BIND_ADDRESS", "127.0.0.1")
    return jsonify({
        "api_key": api_key,
        "bind_address": bind_address
    })

if __name__ == '__main__':
    # Corregido: Modo debug solo en desarrollo
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    # Corregido: Por defecto localhost
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    app.run(debug=debug_mode, host=host)