#!/usr/bin/env python3
"""
📋 CONFIGURAZIONE ESEMPIO - Dashboard Unificata
File di esempio per configurare le variabili d'ambiente
Creato da Ezio Camporeale
"""

# Dashboard Unificata - Configurazione Esempio
# Copia questo file come config_local.py e configura con i tuoi valori

# ==================== DATABASE SUPABASE ====================

# Progetto LEAD
LEAD_SUPABASE_URL = "https://your-lead-project.supabase.co"
LEAD_SUPABASE_KEY = "your-lead-supabase-key"

# Progetto CPA
CPA_SUPABASE_URL = "https://your-cpa-project.supabase.co"
CPA_SUPABASE_KEY = "your-cpa-supabase-key"

# Progetto PROP BROKER
PROP_SUPABASE_URL = "https://your-prop-project.supabase.co"
PROP_SUPABASE_KEY = "your-prop-supabase-key"

# ==================== AI ASSISTANT ====================

# DeepSeek API
DEEPSEEK_API_KEY = "your-deepseek-api-key"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# ==================== AUTENTICAZIONE ====================

# Credenziali Admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your-secure-admin-password"

# Credenziali Manager
MANAGER_USERNAME = "manager"
MANAGER_PASSWORD = "your-secure-manager-password"

# Credenziali Viewer
VIEWER_USERNAME = "viewer"
VIEWER_PASSWORD = "your-secure-viewer-password"

# ==================== CONFIGURAZIONE APP ====================

# App
APP_TITLE = "Dashboard Unificata"
APP_ICON = "🎯"
PAGE_ICON = "🎯"
THEME_COLOR = "#2E86AB"

# ==================== SICUREZZA ====================

# Sessioni
SESSION_TIMEOUT = 3600
MAX_LOGIN_ATTEMPTS = 3
PASSWORD_MIN_LENGTH = 12

# Backup
BACKUP_ENABLED = True
BACKUP_FREQUENCY = "Daily"
BACKUP_RETENTION_DAYS = 30

# ==================== ISTRUZIONI ====================

"""
ISTRUZIONI PER LA CONFIGURAZIONE:

1. Copia questo file come config_local.py
2. Sostituisci tutti i valori "your-*" con i tuoi valori reali
3. NON committare config_local.py su Git
4. Per Streamlit Cloud, configura i secrets nel dashboard

VARIABILI D'AMBIENTE ALTERNATIVE:
Puoi anche usare variabili d'ambiente invece di questo file:

export LEAD_SUPABASE_URL="https://your-lead-project.supabase.co"
export LEAD_SUPABASE_KEY="your-lead-supabase-key"
# ... e così via per tutte le altre variabili

STREAMLIT CLOUD SECRETS:
Configura nel dashboard Streamlit Cloud:
- supabase.lead_url
- supabase.lead_key
- supabase.cpa_url
- supabase.cpa_key
- supabase.prop_url
- supabase.prop_key
- ai.deepseek_api_key
- auth.admin_username
- auth.admin_password
"""
