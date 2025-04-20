#!/usr/bin/env python
"""
Script de demostración para Bandit SAST
"""
import os
import sys
import subprocess
import time

def print_header(text):
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80 + "\n")

def run_command(command, title):
    print_header(title)
    print(f"Ejecutando: {command}\n")
    subprocess.run(command, shell=True)
    time.sleep(1)  # Pausa para mejor visualización

def main():
    # Asegurar que estamos en el directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(script_dir, ".."))
    
    # Comprobar instalación de bandit
    try:
        subprocess.run(["bandit", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Bandit no está instalado. Instalando...")
        subprocess.run(["pip", "install", "bandit"], check=True)
    
    # Ejecutar análisis en la aplicación vulnerable
    run_command(
        "bandit -r examples/vulnerable_app.py -f txt",
        "Análisis de código vulnerable"
    )
    
    # Ejecutar análisis en la aplicación segura
    run_command(
        "bandit -r examples/secure_app.py -f txt",
        "Análisis de código seguro"
    )
    
    # Ejecutar con plugin personalizado
    run_command(
        "bandit -r examples/vulnerable_app.py -p examples/custom_plugins/custom_bandit_checks.py -f txt",
        "Análisis con plugin personalizado"
    )
    
    # Generar reporte HTML
    run_command(
        "bandit
