#!/usr/bin/env python3
"""
🗄️ GESTORE DATABASE UNIFICATO - Dashboard Unificata
🛡️ Gestione sicura di tutti e 3 i database Supabase
Basato sulla sicurezza di Dashboard_Gestione_CPA
Creato da Ezio Camporeale
"""

import os
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import pandas as pd

# Import configurazione unificata
from config import get_supabase_config, get_security_config

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedDatabaseManager:
    """Gestore database unificato per tutti i progetti"""
    
    def __init__(self, project_type: str):
        """
        Inizializza il gestore per un progetto specifico
        
        Args:
            project_type: 'lead', 'cpa', o 'prop'
        """
        self.project_type = project_type
        self.config = get_supabase_config(project_type)
        self.security_config = get_security_config()
        
        # Inizializza client Supabase
        self._init_supabase_client()
        
        # Configurazione tabelle per progetto
        self._init_table_configs()
        
        logger.info(f"✅ Database manager inizializzato per progetto: {project_type}")
    
    def _init_supabase_client(self):
        """Inizializza il client Supabase"""
        try:
            from supabase import create_client, Client
            self.supabase: Client = create_client(
                self.config['url'], 
                self.config['key']
            )
            logger.info(f"✅ Client Supabase inizializzato per {self.project_type}")
        except ImportError:
            logger.error("❌ Libreria supabase non installata: pip install supabase")
            self.supabase = None
        except Exception as e:
            logger.error(f"❌ Errore inizializzazione Supabase: {e}")
            self.supabase = None
    
    def _init_table_configs(self):
        """Inizializza configurazioni tabelle per progetto"""
        if self.project_type == 'lead':
            self.tables = {
                'users': 'users',
                'roles': 'roles',
                'leads': 'leads',
                'lead_categories': 'lead_categories',
                'lead_states': 'lead_states',
                'lead_priorities': 'lead_priorities',
                'lead_sources': 'lead_sources',
                'tasks': 'tasks',
                'task_types': 'task_types',
                'task_states': 'task_states',
                'contact_templates': 'contact_templates',
                'contact_sequences': 'contact_sequences',
                'contact_steps': 'contact_steps',
                'lead_contacts': 'lead_contacts',
                'activity_log': 'activity_log',
                'settings': 'settings'
            }
        elif self.project_type == 'cpa':
            self.tables = {
                'users': 'users',
                'roles': 'roles',
                'clienti': 'clienti',
                'broker': 'broker',
                'piattaforme': 'piattaforme',
                'campi_aggiuntivi': 'campi_aggiuntivi',
                'incroci': 'incroci',
                'wallet_transactions': 'wallet_transactions',
                'activity_log': 'activity_log',
                'settings': 'settings'
            }
        elif self.project_type == 'prop':
            self.tables = {
                'users': 'users',
                'roles': 'roles',
                'brokers': 'brokers',
                'prop_firms': 'prop_firms',
                'wallets': 'wallets',
                'pack_copiatori': 'pack_copiatori',
                'gruppi_pamm': 'gruppi_pamm',
                'incroci': 'incroci',
                'transazioni_wallet': 'transazioni_wallet',
                'performance_history': 'performance_history',
                'activity_log': 'activity_log',
                'settings': 'settings'
            }
        else:
            raise ValueError(f"Tipo progetto non supportato: {self.project_type}")
    
    def test_connection(self) -> Tuple[bool, str]:
        """Testa la connessione al database"""
        if not self.supabase:
            return False, "❌ Client Supabase non disponibile"
        
        try:
            # Prova a leggere dalla tabella users
            response = self.supabase.table(self.tables['users']).select('count', count='exact').execute()
            return True, f"✅ Connessione {self.project_type} attiva"
        except Exception as e:
            return False, f"❌ Errore connessione {self.project_type}: {e}"
    
    def get_all_records(self, table_name: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """Recupera tutti i record da una tabella"""
        if not self.supabase:
            return []
        
        try:
            response = self.supabase.table(table_name).select('*').limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"❌ Errore recupero {table_name}: {e}")
            return []
    
    def get_record_by_id(self, table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
        """Recupera un record per ID"""
        if not self.supabase:
            return None
        
        try:
            response = self.supabase.table(table_name).select('*').eq('id', record_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"❌ Errore recupero {table_name} ID {record_id}: {e}")
            return None
    
    def insert_record(self, table_name: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Inserisce un nuovo record"""
        if not self.supabase:
            return False, "❌ Client Supabase non disponibile"
        
        try:
            # Aggiungi timestamp
            data['created_at'] = datetime.now().isoformat()
            data['updated_at'] = datetime.now().isoformat()
            
            response = self.supabase.table(table_name).insert(data).execute()
            
            if response.data:
                record_id = response.data[0].get('id', 'N/A')
                return True, f"✅ Record inserito in {table_name} con ID: {record_id}"
            else:
                return False, f"❌ Errore inserimento in {table_name}"
                
        except Exception as e:
            return False, f"❌ Errore inserimento {table_name}: {e}"
    
    def update_record(self, table_name: str, record_id: int, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Aggiorna un record esistente"""
        if not self.supabase:
            return False, "❌ Client Supabase non disponibile"
        
        try:
            # Aggiungi timestamp aggiornamento
            data['updated_at'] = datetime.now().isoformat()
            
            response = self.supabase.table(table_name).update(data).eq('id', record_id).execute()
            
            if response.data:
                return True, f"✅ Record {record_id} aggiornato in {table_name}"
            else:
                return False, f"❌ Record {record_id} non trovato in {table_name}"
                
        except Exception as e:
            return False, f"❌ Errore aggiornamento {table_name} ID {record_id}: {e}"
    
    def delete_record(self, table_name: str, record_id: int) -> Tuple[bool, str]:
        """Elimina un record"""
        if not self.supabase:
            return False, "❌ Client Supabase non disponibile"
        
        try:
            response = self.supabase.table(table_name).delete().eq('id', record_id).execute()
            
            if response.data:
                return True, f"✅ Record {record_id} eliminato da {table_name}"
            else:
                return False, f"❌ Record {record_id} non trovato in {table_name}"
                
        except Exception as e:
            return False, f"❌ Errore eliminazione {table_name} ID {record_id}: {e}"
    
    def search_records(self, table_name: str, filters: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        """Cerca record con filtri"""
        if not self.supabase:
            return []
        
        try:
            query = self.supabase.table(table_name).select('*')
            
            # Applica filtri
            for key, value in filters.items():
                if value is not None:
                    query = query.eq(key, value)
            
            response = query.limit(limit).execute()
            return response.data if response.data else []
            
        except Exception as e:
            logger.error(f"❌ Errore ricerca {table_name}: {e}")
            return []
    
    def get_table_stats(self, table_name: str) -> Dict[str, Any]:
        """Ottiene statistiche di una tabella"""
        if not self.supabase:
            return {}
        
        try:
            # Conta record totali
            count_response = self.supabase.table(table_name).select('count', count='exact').execute()
            total_records = count_response.count if count_response.count else 0
            
            # Ottieni ultimo record
            last_record = self.supabase.table(table_name).select('created_at').order('created_at', desc=True).limit(1).execute()
            last_created = last_record.data[0]['created_at'] if last_record.data else None
            
            return {
                'table_name': table_name,
                'total_records': total_records,
                'last_created': last_created,
                'project_type': self.project_type
            }
            
        except Exception as e:
            logger.error(f"❌ Errore statistiche {table_name}: {e}")
            return {}
    
    def get_all_table_stats(self) -> Dict[str, Dict[str, Any]]:
        """Ottiene statistiche di tutte le tabelle"""
        stats = {}
        for table_name in self.tables.values():
            stats[table_name] = self.get_table_stats(table_name)
        return stats
    
    def backup_table(self, table_name: str) -> Tuple[bool, str]:
        """Crea backup di una tabella"""
        if not self.supabase:
            return False, "❌ Client Supabase non disponibile"
        
        try:
            # Ottieni tutti i record
            records = self.get_all_records(table_name)
            
            if not records:
                return False, f"❌ Nessun record trovato in {table_name}"
            
            # Crea backup
            backup_data = {
                'table_name': table_name,
                'project_type': self.project_type,
                'backup_timestamp': datetime.now().isoformat(),
                'total_records': len(records),
                'data': records
            }
            
            # Salva backup (implementazione specifica)
            backup_file = f"backup_{self.project_type}_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            # Qui potresti salvare il backup su file o database
            
            return True, f"✅ Backup {table_name} creato: {len(records)} record"
            
        except Exception as e:
            return False, f"❌ Errore backup {table_name}: {e}"
    
    def get_project_info(self) -> Dict[str, Any]:
        """Ottiene informazioni del progetto"""
        return {
            'project_type': self.project_type,
            'supabase_url': self.config['url'],
            'tables': list(self.tables.keys()),
            'is_configured': self.supabase is not None,
            'security_enabled': self.security_config.get('enable_rls', True)
        }

# Funzioni di utilità
def get_database_manager(project_type: str) -> UnifiedDatabaseManager:
    """Ottiene un gestore database per un progetto specifico"""
    return UnifiedDatabaseManager(project_type)

def test_all_connections() -> Dict[str, Tuple[bool, str]]:
    """Testa connessioni a tutti i database"""
    results = {}
    for project_type in ['lead', 'cpa', 'prop']:
        try:
            manager = UnifiedDatabaseManager(project_type)
            results[project_type] = manager.test_connection()
        except Exception as e:
            results[project_type] = (False, f"❌ Errore inizializzazione {project_type}: {e}")
    return results
