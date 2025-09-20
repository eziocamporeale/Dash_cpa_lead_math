#!/usr/bin/env python3
"""
🔧 CONFIGURAZIONE UNIFICATA - Dashboard Unificata
🛡️ Sistema di configurazione sicuro per tutti e 3 i progetti
Basato sulla sicurezza di Dashboard_Gestione_CPA
Creato da Ezio Camporeale
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedConfig:
    """Configurazione unificata sicura per Streamlit Cloud"""
    
    def __init__(self):
        """Inizializza la configurazione unificata"""
        self.base_dir = Path(__file__).parent.parent
        
        # Configurazione progetti Supabase
        self._init_supabase_configs()
        
        # Configurazione AI Assistant
        self._init_ai_config()
        
        # Configurazione autenticazione
        self._init_auth_config()
        
        # Configurazione app
        self._init_app_config()
        
        # Configurazione sicurezza
        self._init_security_config()
        
        logger.info("✅ Configurazione unificata inizializzata")
    
    def _init_supabase_configs(self):
        """Inizializza configurazioni Supabase per tutti i progetti"""
        # Progetto LEAD
        self.lead_supabase_url = self._get_config('LEAD_SUPABASE_URL')
        self.lead_supabase_key = self._get_config('LEAD_SUPABASE_KEY')
        
        # Progetto CPA
        self.cpa_supabase_url = self._get_config('CPA_SUPABASE_URL')
        self.cpa_supabase_key = self._get_config('CPA_SUPABASE_KEY')
        
        # Progetto PROP BROKER
        self.prop_supabase_url = self._get_config('PROP_SUPABASE_URL')
        self.prop_supabase_key = self._get_config('PROP_SUPABASE_KEY')
    
    def _init_ai_config(self):
        """Inizializza configurazione AI Assistant"""
        self.deepseek_api_key = self._get_config('DEEPSEEK_API_KEY')
        self.deepseek_api_url = self._get_config('DEEPSEEK_API_URL')
        self.deepseek_model = self._get_config('DEEPSEEK_MODEL')
        
        # Configurazione AI Assistant
        self.ai_config = {
            'max_tokens': 1500,
            'temperature': 0.7,
            'timeout': 60,
            'retry_attempts': 3,
            'cache_responses': True,
            'cache_duration_hours': 24
        }
    
    def _init_auth_config(self):
        """Inizializza configurazione autenticazione"""
        self.auth_config = {
            'cookie_name': 'unified_dashboard_auth',
            'cookie_key': 'unified_dashboard_key',
            'cookie_expiry_days': 30,
            'session_timeout': 3600,
            'max_login_attempts': 3,
            'password_min_length': 12,
            'preauthorized': ['admin@unified.com']
        }
        
        # Credenziali admin
        self.admin_username = self._get_config('ADMIN_USERNAME')
        self.admin_password = self._get_config('ADMIN_PASSWORD')
        self.manager_username = self._get_config('MANAGER_USERNAME')
        self.manager_password = self._get_config('MANAGER_PASSWORD')
        self.viewer_username = self._get_config('VIEWER_USERNAME')
        self.viewer_password = self._get_config('VIEWER_PASSWORD')
    
    def _init_app_config(self):
        """Inizializza configurazione app"""
        self.app_title = self._get_config('APP_TITLE', 'Dashboard Unificata')
        self.app_icon = self._get_config('APP_ICON', '🎯')
        self.page_icon = self._get_config('PAGE_ICON', '🎯')
        self.theme_color = self._get_config('THEME_COLOR', '#2E86AB')
        
        # Configurazione UI
        self.ui_config = {
            'sidebar_state': 'expanded',
            'page_layout': 'wide',
            'chart_height': 400,
            'chart_template': 'plotly_white',
            'items_per_page': 20
        }
    
    def _init_security_config(self):
        """Inizializza configurazione sicurezza"""
        self.security_config = {
            'encrypt_passwords': True,
            'enable_rls': True,
            'enable_audit': True,
            'backup_enabled': True,
            'backup_frequency': 'Daily',
            'backup_retention_days': 30,
            'log_level': 'INFO'
        }
    
    def _get_config(self, env_var: str, default: str = None) -> str:
        """Ottiene configurazione da variabili d'ambiente o Streamlit secrets"""
        # 1. Prova variabili d'ambiente locali
        value = os.getenv(env_var)
        if value:
            logger.info(f"✅ Configurazione {env_var} da variabili d'ambiente")
            return value
        
        # 2. Prova Streamlit secrets (per deployment)
        try:
            import streamlit as st
            if hasattr(st, 'secrets'):
                # Prova diversi percorsi nei secrets
                secrets_paths = [
                    f'supabase.{env_var.lower()}',
                    f'ai.{env_var.lower()}',
                    f'auth.{env_var.lower()}',
                    f'app.{env_var.lower()}',
                    env_var.lower()
                ]
                
                for path in secrets_paths:
                    try:
                        value = st.secrets[path]
                        if value:
                            logger.info(f"✅ Configurazione {env_var} da Streamlit secrets: {path}")
                            return value
                    except:
                        continue
        except ImportError:
            pass
        
        # 3. Usa default se disponibile
        if default:
            logger.warning(f"⚠️ Usando configurazione default per {env_var}")
            return default
        
        # 4. Errore se non trovato
        raise ValueError(f"Configurazione {env_var} non trovata")
    
    def get_supabase_config(self, project_type: str) -> Dict[str, str]:
        """Ottiene configurazione Supabase per un progetto specifico"""
        if project_type == 'lead':
            return {
                'url': self.lead_supabase_url,
                'key': self.lead_supabase_key
            }
        elif project_type == 'cpa':
            return {
                'url': self.cpa_supabase_url,
                'key': self.cpa_supabase_key
            }
        elif project_type == 'prop':
            return {
                'url': self.prop_supabase_url,
                'key': self.prop_supabase_key
            }
        else:
            raise ValueError(f"Tipo progetto non supportato: {project_type}")
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Ottiene configurazione AI Assistant"""
        return {
            'api_key': self.deepseek_api_key,
            'api_url': self.deepseek_api_url,
            'model': self.deepseek_model,
            'config': self.ai_config
        }
    
    def get_auth_config(self) -> Dict[str, Any]:
        """Ottiene configurazione autenticazione"""
        return self.auth_config
    
    def get_app_config(self) -> Dict[str, Any]:
        """Ottiene configurazione app"""
        return {
            'title': self.app_title,
            'icon': self.app_icon,
            'page_icon': self.page_icon,
            'theme_color': self.theme_color,
            'ui': self.ui_config
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Ottiene configurazione sicurezza"""
        return self.security_config
    
    def is_configured(self) -> bool:
        """Verifica se la configurazione è completa"""
        try:
            # Verifica configurazioni Supabase
            self.get_supabase_config('lead')
            self.get_supabase_config('cpa')
            self.get_supabase_config('prop')
            
            # Verifica configurazione AI
            self.get_ai_config()
            
            # Verifica configurazione auth
            self.get_auth_config()
            
            return True
        except Exception as e:
            logger.error(f"❌ Configurazione incompleta: {e}")
            return False

# Istanza globale della configurazione
config = UnifiedConfig()

# Funzioni di utilità
def get_config() -> UnifiedConfig:
    """Ottiene l'istanza della configurazione"""
    return config

def get_supabase_config(project_type: str) -> Dict[str, str]:
    """Ottiene configurazione Supabase per un progetto"""
    return config.get_supabase_config(project_type)

def get_ai_config() -> Dict[str, Any]:
    """Ottiene configurazione AI Assistant"""
    return config.get_ai_config()

def get_auth_config() -> Dict[str, Any]:
    """Ottiene configurazione autenticazione"""
    return config.get_auth_config()

def get_app_config() -> Dict[str, Any]:
    """Ottiene configurazione app"""
    return config.get_app_config()

def get_security_config() -> Dict[str, Any]:
    """Ottiene configurazione sicurezza"""
    return config.get_security_config()
