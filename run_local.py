#!/usr/bin/env python3
"""
🏠 RUN LOCAL - Dashboard Unificata
Script per eseguire la dashboard in locale
Creato da Ezio Camporeale
"""

import os
import sys
import subprocess
import streamlit as st

def check_requirements():
    """Controlla se i requirements sono installati"""
    try:
        import streamlit
        import pandas
        import plotly
        import supabase
        import requests
        import bcrypt
        print("✅ Tutti i requirements sono installati")
        return True
    except ImportError as e:
        print(f"❌ Modulo mancante: {e}")
        print("📦 Installa i requirements con: pip install -r requirements.txt")
        return False

def check_config():
    """Controlla se la configurazione è presente"""
    config_files = [
        '.streamlit/config.toml',
        '.streamlit/secrets.toml',
        'config_example.py'
    ]
    
    missing_files = []
    for file in config_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️ File di configurazione mancanti: {missing_files}")
        print("📝 Copia config_example.py come config_local.py e configura")
        return False
    
    print("✅ Configurazione presente")
    return True

def setup_environment():
    """Configura l'ambiente"""
    # Crea directory .streamlit se non esiste
    if not os.path.exists('.streamlit'):
        os.makedirs('.streamlit')
        print("📁 Creata directory .streamlit")
    
    # Crea file secrets.toml se non esiste
    if not os.path.exists('.streamlit/secrets.toml'):
        print("⚠️ File .streamlit/secrets.toml mancante")
        print("📝 Copia i tuoi secrets da config_example.py")
        return False
    
    return True

def run_dashboard():
    """Esegue la dashboard"""
    try:
        print("🚀 Avvio Dashboard Unificata...")
        print("🌐 Apri il browser su: http://localhost:8501")
        print("⏹️ Premi Ctrl+C per fermare")
        
        # Esegui streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false'
        ])
        
    except KeyboardInterrupt:
        print("\n⏹️ Dashboard fermata")
    except Exception as e:
        print(f"❌ Errore: {e}")

def main():
    """Funzione principale"""
    print("🎯 Dashboard Unificata - Run Local")
    print("=" * 50)
    
    # Controlli preliminari
    if not check_requirements():
        return
    
    if not setup_environment():
        return
    
    if not check_config():
        return
    
    print("\n✅ Tutto pronto!")
    print("🚀 Avvio dashboard...")
    
    # Esegui dashboard
    run_dashboard()

if __name__ == "__main__":
    main()
