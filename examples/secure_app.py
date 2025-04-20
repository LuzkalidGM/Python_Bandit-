import os
import yaml
import pickle
import subprocess
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Solución 1: Variables de entorno para credenciales
import os
DB_PASSWORD = os.environ.get('DB_PASSWORD')

@app.route('/process')
def process_data():
    user_input = request.args.get('command')
    # Solución 2: Lista blanca de comandos permitidos
    allowed_commands = ['date', 'uptime', 'whoami']
    if user_input in allowed_commands:
        result = subprocess.run([user_input], capture_output=True, text=True, shell=False)
        return result.stdout
    return "Comando no permitido"

@app.route('/load_config')
def load_config():
    config_file = request.args.get('file')
    # Solución 3: Uso de yaml.safe_load y validación de ruta
    import os.path
    config_dir = '/safe/config/path'
    if not os.path.abspath(config_file).startswith(config_dir):
        return "Acceso denegado"
    with open(os.path.join(config_dir, os.path.basename(config_file)), 'r') as f:
        config = yaml.safe_load(f)
    return str(config)

@app.route('/load_data')
def load_data():
    # Solución 4: Formatos de serialización seguros
    data_file = request.args.get('file')
    import json
    with open(data_file, 'r') as f:
        data = json.load(f)
    return str(data)

@app.route('/execute')
def execute_command():
    cmd = request.args.get('cmd')
    # Solución 5: Lista blanca con argumentos separados
    allowed_commands = {'date': ['date'], 'uptime': ['uptime']}
    if cmd in allowed_commands:
        output = subprocess.check_output(allowed_commands[cmd], shell=False)
        return output
    return "Comando no permitido"

@app.route('/get_user/<username>')
def get_user(username):
    # Solución 6: Parametrización de consultas SQL
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return str(cursor.fetchone())

if __name__ == '__main__':
    # Solución 7: Configuración segura para producción
    app.run(debug=False, host='127.0.0.1')
