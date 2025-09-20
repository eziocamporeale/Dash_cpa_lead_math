#!/usr/bin/env python3
"""
🔐 SISTEMA AUTENTICAZIONE UNIFICATO - Dashboard Unificata
🛡️ Autenticazione sicura per tutti e 3 i progetti
Basato sulla sicurezza di Dashboard_Gestione_CPA
Creato da Ezio Camporeale
"""

import streamlit as st
import hashlib
import secrets
import logging
from typing import Dict, Optional, Tuple, Any
from datetime import datetime, timedelta
import bcrypt

# Import configurazione e database
from config import get_auth_config, get_security_config
from database import get_database_manager

# Configurazione logging
logger = logging.getLogger(__name__)

class UnifiedAuthSystem:
    """Sistema di autenticazione unificato per tutti i progetti"""
    
    def __init__(self):
        """Inizializza il sistema di autenticazione"""
        self.auth_config = get_auth_config()
        self.security_config = get_security_config()
        
        # Database managers per tutti i progetti
        self.db_managers = {
            'lead': get_database_manager('lead'),
            'cpa': get_database_manager('cpa'),
            'prop': get_database_manager('prop')
        }
        
        # Inizializza sessioni
        self._init_session_state()
        
        logger.info("✅ Sistema autenticazione unificato inizializzato")
    
    def _init_session_state(self):
        """Inizializza lo stato della sessione"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_info' not in st.session_state:
            st.session_state.user_info = {}
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
        if 'last_login_attempt' not in st.session_state:
            st.session_state.last_login_attempt = None
        if 'current_project' not in st.session_state:
            st.session_state.current_project = 'lead'
    
    def hash_password(self, password: str) -> str:
        """Hash della password con salt (sicuro come CPA)"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${password_hash}"
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Verifica password con supporto per formati multipli (da CPA)"""
        try:
            # Se è un hash bcrypt (inizia con $2b$)
            if stored_hash.startswith('$2b$'):
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
            
            # Se è un hash semplice (per test e admin hardcoded)
            elif stored_hash == password:
                return True
            
            # Se è un hash con salt (SHA256 con salt)
            elif '$' in stored_hash and len(stored_hash) > 50:
                salt, hash_part = stored_hash.split('$', 1)
                password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
                return password_hash == hash_part
            
            # Se è un hash SHA256 semplice (senza salt, 64 caratteri)
            elif len(stored_hash) == 64:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                return password_hash == stored_hash
            
            # Fallback: confronto diretto
            else:
                return password == stored_hash
                
        except Exception as e:
            logger.error(f"Errore verifica password: {e}")
            return False
    
    def check_rate_limit(self) -> bool:
        """Controlla il rate limiting (da CPA)"""
        max_attempts = self.auth_config.get('max_login_attempts', 3)
        
        if st.session_state.login_attempts >= max_attempts:
            if st.session_state.last_login_attempt:
                time_diff = datetime.now() - st.session_state.last_login_attempt
                if time_diff < timedelta(minutes=15):  # Blocco per 15 minuti
                    return False
        
        return True
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Autentica un utente (logica unificata)"""
        try:
            # Controlla rate limiting
            if not self.check_rate_limit():
                return False, "❌ Troppi tentativi di login. Riprova tra 15 minuti.", {}
            
            # Cerca l'utente in tutti i database
            user_data = None
            project_found = None
            
            for project_type, db_manager in self.db_managers.items():
                try:
                    response = db_manager.supabase.table('users').select('*').eq('username', username).execute()
                    
                    if response.data:
                        user_data = response.data[0]
                        project_found = project_type
                        break
                except Exception as e:
                    logger.warning(f"Errore ricerca utente in {project_type}: {e}")
                    continue
            
            if not user_data:
                self._increment_login_attempts()
                return False, "❌ Utente non trovato", {}
            
            # Verifica password
            stored_hash = user_data.get('password_hash', '')
            if not self.verify_password(password, stored_hash):
                self._increment_login_attempts()
                return False, "❌ Password errata", {}
            
            # Login riuscito
            self._reset_login_attempts()
            self._set_user_session(user_data, project_found)
            
            logger.info(f"✅ Autenticazione riuscita per {username} in progetto {project_found}")
            return True, f"✅ Benvenuto {user_data.get('first_name', username)}!", user_data
            
        except Exception as e:
            logger.error(f"Errore autenticazione: {e}")
            return False, f"❌ Errore sistema: {e}", {}
    
    def _increment_login_attempts(self):
        """Incrementa i tentativi di login"""
        st.session_state.login_attempts += 1
        st.session_state.last_login_attempt = datetime.now()
    
    def _reset_login_attempts(self):
        """Reset dei tentativi di login"""
        st.session_state.login_attempts = 0
        st.session_state.last_login_attempt = None
    
    def _set_user_session(self, user_data: Dict[str, Any], project_type: str):
        """Imposta la sessione utente"""
        st.session_state.authenticated = True
        st.session_state.user_info = {
            'id': user_data.get('id'),
            'username': user_data.get('username'),
            'email': user_data.get('email'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'role': user_data.get('role'),
            'project_type': project_type,
            'login_time': datetime.now().isoformat()
        }
        st.session_state.current_project = project_type
    
    def logout_user(self):
        """Logout dell'utente"""
        st.session_state.authenticated = False
        st.session_state.user_info = {}
        st.session_state.current_project = 'lead'
        logger.info("✅ Utente disconnesso")
    
    def is_authenticated(self) -> bool:
        """Verifica se l'utente è autenticato"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self) -> Dict[str, Any]:
        """Ottiene le informazioni dell'utente corrente"""
        return st.session_state.get('user_info', {})
    
    def get_current_project(self) -> str:
        """Ottiene il progetto corrente"""
        return st.session_state.get('current_project', 'lead')
    
    def switch_project(self, project_type: str):
        """Cambia il progetto corrente"""
        if project_type in ['lead', 'cpa', 'prop']:
            st.session_state.current_project = project_type
            logger.info(f"✅ Progetto cambiato a: {project_type}")
    
    def check_permissions(self, required_permission: str) -> bool:
        """Verifica i permessi dell'utente"""
        if not self.is_authenticated():
            return False
        
        user_info = self.get_current_user()
        user_role = user_info.get('role', 'viewer')
        
        # Permessi per ruolo
        permissions = {
            'admin': ['all'],
            'manager': ['read', 'write', 'delete', 'manage_team'],
            'user': ['read', 'write'],
            'viewer': ['read']
        }
        
        user_permissions = permissions.get(user_role, ['read'])
        
        return 'all' in user_permissions or required_permission in user_permissions
    
    def require_auth(self, required_permission: str = 'read'):
        """Decorator per richiedere autenticazione"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.is_authenticated():
                    st.error("❌ Accesso negato. Effettua il login.")
                    return
                
                if not self.check_permissions(required_permission):
                    st.error(f"❌ Permessi insufficienti. Richiesto: {required_permission}")
                    return
                
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Istanza globale del sistema di autenticazione
auth_system = UnifiedAuthSystem()

# Funzioni di utilità
def require_auth(permission: str = 'read'):
    """Decorator per richiedere autenticazione"""
    return auth_system.require_auth(permission)

def get_current_user() -> Dict[str, Any]:
    """Ottiene l'utente corrente"""
    return auth_system.get_current_user()

def get_current_project() -> str:
    """Ottiene il progetto corrente"""
    return auth_system.get_current_project()

def switch_project(project_type: str):
    """Cambia il progetto corrente"""
    auth_system.switch_project(project_type)

def is_authenticated() -> bool:
    """Verifica se l'utente è autenticato"""
    return auth_system.is_authenticated()

def logout():
    """Logout dell'utente"""
    auth_system.logout_user()

def authenticate(username: str, password: str) -> Tuple[bool, str, Dict[str, Any]]:
    """Autentica un utente"""
    return auth_system.authenticate_user(username, password)
