#!/usr/bin/env python3
"""
🔐 FORM DI LOGIN UNIFICATO - Dashboard Unificata
Form di login per tutti e 3 i progetti
Creato da Ezio Camporeale
"""

import streamlit as st
from auth import authenticate, is_authenticated, get_current_user, logout

def render_login_form():
    """Rende il form di login unificato"""
    if is_authenticated():
        render_logout_section()
        return
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>🎯 Dashboard Unificata</h1>
        <p>Accedi per gestire i tuoi progetti</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("login_form"):
                st.markdown("### 🔐 Accesso")
                
                username = st.text_input(
                    "👤 Username",
                    placeholder="Inserisci il tuo username",
                    help="Username per accedere al sistema"
                )
                
                password = st.text_input(
                    "🔒 Password",
                    type="password",
                    placeholder="Inserisci la tua password",
                    help="Password per accedere al sistema"
                )
                
                col_submit1, col_submit2 = st.columns(2)
                
                with col_submit1:
                    login_button = st.form_submit_button(
                        "🚀 Accedi",
                        use_container_width=True,
                        type="primary"
                    )
                
                with col_submit2:
                    demo_button = st.form_submit_button(
                        "🧪 Demo",
                        use_container_width=True
                    )
                
                if login_button:
                    if username and password:
                        success, message, user_data = authenticate(username, password)
                        
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("❌ Inserisci username e password")
                
                if demo_button:
                    # Login demo con credenziali di test
                    success, message, user_data = authenticate("admin", "admin123")
                    if success:
                        st.success("✅ Accesso demo completato")
                        st.rerun()
                    else:
                        st.error("❌ Errore accesso demo")

def render_logout_section():
    """Rende la sezione di logout"""
    user_info = get_current_user()
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); 
                    color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h4>👋 Benvenuto, {user_info.get('first_name', user_info.get('username', 'Utente'))}!</h4>
            <p>Progetto: {user_info.get('project_type', 'lead').upper()}</p>
            <p>Ruolo: {user_info.get('role', 'user').title()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Cambia Progetto", use_container_width=True):
            st.session_state.show_project_selector = True
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    
    # Selettore progetto
    if st.session_state.get('show_project_selector', False):
        render_project_selector()

def render_project_selector():
    """Rende il selettore di progetto"""
    st.markdown("### 🎯 Seleziona Progetto")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 LEAD", use_container_width=True):
            from auth import switch_project
            switch_project('lead')
            st.session_state.show_project_selector = False
            st.rerun()
    
    with col2:
        if st.button("💼 CPA", use_container_width=True):
        from auth import switch_project
        switch_project('cpa')
        st.session_state.show_project_selector = False
        st.rerun()
    
    with col3:
        if st.button("🧮 PROP", use_container_width=True):
            from auth import switch_project
            switch_project('prop')
            st.session_state.show_project_selector = False
            st.rerun()
    
    if st.button("❌ Annulla", use_container_width=True):
        st.session_state.show_project_selector = False
        st.rerun()

def render_auth_guard():
    """Rende la guardia di autenticazione"""
    if not is_authenticated():
        render_login_form()
        return False
    return True

def render_user_info():
    """Rende le informazioni utente"""
    if not is_authenticated():
        return
    
    user_info = get_current_user()
    
    with st.sidebar:
        st.markdown("### 👤 Informazioni Utente")
        st.write(f"**Nome:** {user_info.get('first_name', 'N/A')}")
        st.write(f"**Email:** {user_info.get('email', 'N/A')}")
        st.write(f"**Ruolo:** {user_info.get('role', 'N/A')}")
        st.write(f"**Progetto:** {user_info.get('project_type', 'N/A')}")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
