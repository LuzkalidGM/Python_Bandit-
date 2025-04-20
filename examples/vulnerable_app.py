import os
import yaml
import pickle
import subprocess
from flask import Flask, request

app = Flask(__name__)

# Vulnerabilidad 1: Credenciales hardcoded
DB_PASSWORD = "super_secret_password123"

@app.route('/process')
def process_data():
    user_input = request.args.get('command')
    # Vulnerabilidad 2: Inyección de comandos
    result = os.system(user_input)
    return str(result)

@app.route('/load_config')
def load_config():
    config_file = request.args.get('file')
    # Vulnerabilidad 3: Deserialización YAML insegura
    with open(config_file, 'r') as f:
        config = yaml.load(f)
    return str(config)

@app.route('/load_data')
def load_data():
    data_file = request.args.get('file')
    # Vulnerabilidad 4: Deserialización Pickle insegura
    with open(data_file, 'rb') as f:
        data = pickle.load(f)
    return str(data)

@app.route('/execute')
def execute_command():
    cmd = request.args.get('cmd')
    # Vulnerabilidad 5: Inyección de comandos con shell=True
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/get_user/<username>')
def get_user(username):
    # Vulnerabilidad 6: SQL Injection
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return str(cursor.fetchone())

if __name__ == '__main__':
    # Vulnerabilidad 7: Modo debug en producción
    app.run(debug=True, host='0.0.0.0')
