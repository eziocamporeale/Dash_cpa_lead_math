#!/usr/bin/env python3
"""
🧭 NAVIGAZIONE UNIFICATA - Dashboard Unificata
Sistema di navigazione per tutti e 3 i progetti
Creato da Ezio Camporeale
"""

import streamlit as st
from auth import get_current_project, get_current_user, switch_project

def render_sidebar_navigation():
    """Rende la navigazione nella sidebar"""
    user_info = get_current_user()
    current_project = get_current_project()
    
    st.sidebar.markdown("### 🎯 Dashboard Unificata")
    
    # Selettore progetto
    st.sidebar.markdown("#### 📋 Progetti")
    
    project_options = {
        'lead': '🎯 LEAD',
        'cpa': '💼 CPA', 
        'prop': '🧮 PROP BROKER'
    }
    
    selected_project = st.sidebar.selectbox(
        "Seleziona Progetto",
        options=list(project_options.keys()),
        format_func=lambda x: project_options[x],
        index=list(project_options.keys()).index(current_project)
    )
    
    if selected_project != current_project:
        switch_project(selected_project)
        st.rerun()
    
    # Menu di navigazione per progetto
    render_project_menu(current_project)
    
    # Informazioni utente
    render_user_sidebar_info()

def render_project_menu(project_type: str):
    """Rende il menu per il progetto specifico"""
    st.sidebar.markdown("#### 🧭 Navigazione")
    
    if project_type == 'lead':
        render_lead_menu()
    elif project_type == 'cpa':
        render_cpa_menu()
    elif project_type == 'prop':
        render_prop_menu()

def render_lead_menu():
    """Rende il menu per il progetto LEAD"""
    menu_items = [
        ("🏠 Dashboard", "dashboard"),
        ("🎯 Lead Management", "leads"),
        ("📋 Task Management", "tasks"),
        ("📞 Sequenze Contatto", "sequences"),
        ("📧 Template", "templates"),
        ("👥 Gestione Gruppi", "groups"),
        ("🔗 Broker Links", "broker_links"),
        ("📜 Scripts", "scripts"),
        ("📁 Storage", "storage"),
        ("🤖 AI Assistant", "ai_assistant"),
        ("📊 Analytics", "analytics"),
        ("⚙️ Impostazioni", "settings")
    ]
    
    for item_name, item_key in menu_items:
        if st.sidebar.button(item_name, use_container_width=True):
            st.session_state.current_page = item_key
            st.rerun()

def render_cpa_menu():
    """Rende il menu per il progetto CPA"""
    menu_items = [
        ("🏠 Dashboard", "dashboard"),
        ("💼 Gestione Clienti", "clients"),
        ("🏦 Gestione Broker", "brokers"),
        ("🔄 Sistema Incroci", "incroci"),
        ("💰 Wallet Management", "wallets"),
        ("📊 Transazioni", "transactions"),
        ("🔗 Broker Links", "broker_links"),
        ("🤖 AI Assistant", "ai_assistant"),
        ("📊 Analytics", "analytics"),
        ("🛡️ Sicurezza", "security"),
        ("⚙️ Impostazioni", "settings")
    ]
    
    for item_name, item_key in menu_items:
        if st.sidebar.button(item_name, use_container_width=True):
            st.session_state.current_page = item_key
            st.rerun()

def render_prop_menu():
    """Rende il menu per il progetto PROP BROKER"""
    menu_items = [
        ("🏠 Dashboard", "dashboard"),
        ("🧮 Gestione Broker", "brokers"),
        ("🏛️ Prop Firm", "prop_firms"),
        ("💰 Wallet Crypto", "wallets"),
        ("📦 Pack Copiatori", "pack_copiatori"),
        ("👥 Gruppi PAMM", "gruppi_pamm"),
        ("🔄 Sistema Incroci", "incroci"),
        ("📊 Performance History", "performance"),
        ("🤖 AI Assistant", "ai_assistant"),
        ("📊 Analytics", "analytics"),
        ("⚙️ Impostazioni", "settings")
    ]
    
    for item_name, item_key in menu_items:
        if st.sidebar.button(item_name, use_container_width=True):
            st.session_state.current_page = item_key
            st.rerun()

def render_user_sidebar_info():
    """Rende le informazioni utente nella sidebar"""
    user_info = get_current_user()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 👤 Utente")
    
    st.sidebar.write(f"**Nome:** {user_info.get('first_name', 'N/A')}")
    st.sidebar.write(f"**Ruolo:** {user_info.get('role', 'N/A')}")
    st.sidebar.write(f"**Progetto:** {user_info.get('project_type', 'N/A').upper()}")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        from auth import logout
        logout()
        st.rerun()

def render_top_navigation():
    """Rende la navigazione superiore"""
    current_project = get_current_project()
    
    # Header con informazioni progetto
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        project_names = {
            'lead': '🎯 LEAD MANAGEMENT',
            'cpa': '💼 CPA MANAGEMENT',
            'prop': '🧮 PROP BROKER MANAGEMENT'
        }
        
        st.markdown(f"### {project_names.get(current_project, 'UNKNOWN PROJECT')}")
    
    with col2:
        # Pulsante cambio progetto rapido
        if st.button("🔄 Cambia Progetto"):
            st.session_state.show_project_selector = True
    
    with col3:
        # Pulsante impostazioni
        if st.button("⚙️ Impostazioni"):
            st.session_state.current_page = 'settings'

def render_breadcrumb():
    """Rende il breadcrumb di navigazione"""
    current_page = st.session_state.get('current_page', 'dashboard')
    current_project = get_current_project()
    
    # Mappa nomi pagine
    page_names = {
        'dashboard': 'Dashboard',
        'leads': 'Lead Management',
        'clients': 'Gestione Clienti',
        'brokers': 'Gestione Broker',
        'tasks': 'Task Management',
        'sequences': 'Sequenze Contatto',
        'templates': 'Template',
        'groups': 'Gestione Gruppi',
        'broker_links': 'Broker Links',
        'scripts': 'Scripts',
        'storage': 'Storage',
        'incroci': 'Sistema Incroci',
        'wallets': 'Wallet Management',
        'transactions': 'Transazioni',
        'pack_copiatori': 'Pack Copiatori',
        'gruppi_pamm': 'Gruppi PAMM',
        'performance': 'Performance History',
        'ai_assistant': 'AI Assistant',
        'analytics': 'Analytics',
        'security': 'Sicurezza',
        'settings': 'Impostazioni'
    }
    
    project_names = {
        'lead': 'LEAD',
        'cpa': 'CPA',
        'prop': 'PROP BROKER'
    }
    
    breadcrumb = f"🏠 {project_names.get(current_project, 'UNKNOWN')} > {page_names.get(current_page, 'Unknown')}"
    
    st.markdown(f"**{breadcrumb}**")
    st.markdown("---")

def render_project_selector_modal():
    """Rende il selettore di progetto in modal"""
    if st.session_state.get('show_project_selector', False):
        st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.5); z-index: 1000; display: flex; 
                    align-items: center; justify-content: center;">
            <div style="background: white; padding: 2rem; border-radius: 10px; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                <h3>🎯 Seleziona Progetto</h3>
                <p>Scegli il progetto su cui vuoi lavorare:</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎯 LEAD", use_container_width=True):
                switch_project('lead')
                st.session_state.show_project_selector = False
                st.rerun()
        
        with col2:
            if st.button("💼 CPA", use_container_width=True):
                switch_project('cpa')
                st.session_state.show_project_selector = False
                st.rerun()
        
        with col3:
            if st.button("🧮 PROP", use_container_width=True):
                switch_project('prop')
                st.session_state.show_project_selector = False
                st.rerun()
        
        if st.button("❌ Annulla", use_container_width=True):
            st.session_state.show_project_selector = False
            st.rerun()

def render_quick_actions():
    """Rende le azioni rapide"""
    current_project = get_current_project()
    
    st.markdown("#### ⚡ Azioni Rapide")
    
    if current_project == 'lead':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Nuovo Lead", use_container_width=True):
                st.session_state.current_page = 'leads'
                st.session_state.show_new_form = True
                st.rerun()
        with col2:
            if st.button("📋 Nuovo Task", use_container_width=True):
                st.session_state.current_page = 'tasks'
                st.session_state.show_new_form = True
                st.rerun()
    
    elif current_project == 'cpa':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Nuovo Cliente", use_container_width=True):
                st.session_state.current_page = 'clients'
                st.session_state.show_new_form = True
                st.rerun()
        with col2:
            if st.button("🔄 Nuovo Incrocio", use_container_width=True):
                st.session_state.current_page = 'incroci'
                st.session_state.show_new_form = True
                st.rerun()
    
    elif current_project == 'prop':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Nuovo Broker", use_container_width=True):
                st.session_state.current_page = 'brokers'
                st.session_state.show_new_form = True
                st.rerun()
        with col2:
            if st.button("🏛️ Nuova Prop Firm", use_container_width=True):
                st.session_state.current_page = 'prop_firms'
                st.session_state.show_new_form = True
                st.rerun()

# Funzioni di utilità
def get_current_page() -> str:
    """Ottiene la pagina corrente"""
    return st.session_state.get('current_page', 'dashboard')

def set_current_page(page: str):
    """Imposta la pagina corrente"""
    st.session_state.current_page = page

def render_navigation():
    """Rende tutta la navigazione"""
    render_sidebar_navigation()
    render_top_navigation()
    render_breadcrumb()
    render_project_selector_modal()
    render_quick_actions()
