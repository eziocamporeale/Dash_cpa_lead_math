#!/usr/bin/env python3
"""
🧪 TEST CONNESSIONI DATABASE - Dashboard Unificata
Testa le connessioni a tutti e 3 i database Supabase
Creato da Ezio Camporeale
"""

import sys
from pathlib import Path

# Aggiungi il percorso del progetto al path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from database import test_all_connections, get_database_manager

def main():
    """Funzione principale per testare le connessioni"""
    print("🧪 TEST CONNESSIONI DATABASE UNIFICATE")
    print("=" * 50)
    
    # Testa tutte le connessioni
    results = test_all_connections()
    
    print("\n📊 RISULTATI TEST:")
    print("-" * 30)
    
    for project_type, (success, message) in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {project_type.upper()}: {message}")
    
    # Test dettagliato per ogni progetto
    print("\n🔍 TEST DETTAGLIATO:")
    print("-" * 30)
    
    for project_type in ['lead', 'cpa', 'prop']:
        try:
            print(f"\n📋 Progetto: {project_type.upper()}")
            manager = get_database_manager(project_type)
            
            # Test connessione
            success, message = manager.test_connection()
            print(f"   Connessione: {message}")
            
            if success:
                # Test statistiche tabelle
                stats = manager.get_all_table_stats()
                print(f"   Tabelle disponibili: {len(stats)}")
                
                for table_name, table_stats in stats.items():
                    if table_stats:
                        print(f"     - {table_name}: {table_stats.get('total_records', 0)} record")
            
        except Exception as e:
            print(f"   ❌ Errore: {e}")
    
    print("\n🎯 TEST COMPLETATO")

if __name__ == "__main__":
    main()
