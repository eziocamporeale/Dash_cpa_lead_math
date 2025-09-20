#!/usr/bin/env python3
"""
🚀 DASHBOARD UNIFICATA - App Principale
Dashboard unificata per LEAD, CPA e PROP BROKER
Creato da Ezio Camporeale
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import sys
import os

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importazioni moduli unificati
from config.unified_config import UnifiedConfig
from database.unified_database_manager import UnifiedDatabaseManager
from auth.unified_auth import UnifiedAuthSystem
from ai.unified_ai_assistant import UnifiedAIAssistant
from components.navigation import UnifiedNavigation
from components.unified_components import UnifiedForm, UnifiedTable, UnifiedChart

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedDashboard:
    """
    🎯 Dashboard Unificata
    
    Integra tutti e tre i progetti:
    - LEAD: Gestione Lead
    - CPA: Gestione CPA
    - PROP: Prop Broker
    """
    
    def __init__(self):
        """Inizializza la dashboard unificata"""
        self.config = UnifiedConfig()
        self.auth_system = UnifiedAuthSystem()
        self.ai_assistant = UnifiedAIAssistant()
        self.navigation = UnifiedNavigation()
        
        # Database managers per ogni progetto
        self.db_managers = {
            'lead': UnifiedDatabaseManager('lead'),
            'cpa': UnifiedDatabaseManager('cpa'),
            'prop': UnifiedDatabaseManager('prop')
        }
        
        # Inizializza session state
        self._init_session_state()
        
        logger.info("🚀 Dashboard Unificata inizializzata")
    
    def _init_session_state(self):
        """Inizializza session state"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'current_project' not in st.session_state:
            st.session_state.current_project = 'lead'
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'dashboard'
        if 'ai_cache' not in st.session_state:
            st.session_state.ai_cache = {}
    
    def run(self):
        """Esegue la dashboard"""
        try:
            # Configurazione pagina
            self._setup_page_config()
            
            # Controllo autenticazione
            if not st.session_state.authenticated:
                self._show_login_page()
                return
            
            # Layout principale
            self._render_main_layout()
            
        except Exception as e:
            logger.error(f"Errore dashboard: {str(e)}")
            st.error(f"❌ Errore: {str(e)}")
    
    def _setup_page_config(self):
        """Configura la pagina Streamlit"""
        st.set_page_config(
            page_title=self.config.app_title,
            page_icon=self.config.app_icon,
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/eziocamporeale/Dash_cpa_lead_math',
                'Report a bug': 'https://github.com/eziocamporeale/Dash_cpa_lead_math/issues',
                'About': f"""
                # {self.config.app_title}
                
                Dashboard unificata per la gestione di:
                - **LEAD**: Gestione Lead
                - **CPA**: Gestione CPA  
                - **PROP**: Prop Broker
                
                Creato da Ezio Camporeale
                """
            }
        )
    
    def _show_login_page(self):
        """Mostra pagina di login"""
        st.title("🔐 Accesso Dashboard Unificata")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### Inserisci le credenziali")
            
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Inserisci username")
                password = st.text_input("🔒 Password", type="password", placeholder="Inserisci password")
                project_type = st.selectbox(
                    "📁 Progetto",
                    options=['lead', 'cpa', 'prop'],
                    format_func=lambda x: {
                        'lead': '🎯 LEAD - Gestione Lead',
                        'cpa': '💰 CPA - Gestione CPA',
                        'prop': '🏢 PROP - Prop Broker'
                    }[x]
                )
                
                submitted = st.form_submit_button("🚀 Accedi", use_container_width=True)
                
                if submitted:
                    if self._authenticate_user(username, password, project_type):
                        st.success("✅ Accesso effettuato con successo!")
                        st.rerun()
                    else:
                        st.error("❌ Credenziali non valide!")
    
    def _authenticate_user(self, username: str, password: str, project_type: str) -> bool:
        """Autentica l'utente"""
        try:
            user_data = self.auth_system.authenticate_user(username, password, project_type)
            if user_data:
                st.session_state.authenticated = True
                st.session_state.user_role = user_data.get('role', 'viewer')
                st.session_state.current_project = project_type
                return True
            return False
        except Exception as e:
            logger.error(f"Errore autenticazione: {str(e)}")
            return False
    
    def _render_main_layout(self):
        """Renderizza layout principale"""
        # Sidebar navigation
        with st.sidebar:
            self._render_sidebar()
        
        # Main content area
        self._render_main_content()
    
    def _render_sidebar(self):
        """Renderizza sidebar"""
        st.markdown(f"# {self.config.app_icon} {self.config.app_title}")
        
        # Info utente
        st.markdown(f"**👤 Utente:** {st.session_state.user_role}")
        st.markdown(f"**📁 Progetto:** {st.session_state.current_project.upper()}")
        
        st.divider()
        
        # Navigazione progetti
        st.markdown("### 📁 Progetti")
        project_options = {
            'lead': '🎯 LEAD',
            'cpa': '💰 CPA',
            'prop': '🏢 PROP'
        }
        
        selected_project = st.selectbox(
            "Seleziona progetto",
            options=list(project_options.keys()),
            format_func=lambda x: project_options[x],
            index=list(project_options.keys()).index(st.session_state.current_project)
        )
        
        if selected_project != st.session_state.current_project:
            st.session_state.current_project = selected_project
            st.rerun()
        
        st.divider()
        
        # Navigazione pagine
        st.markdown("### 🧭 Navigazione")
        
        pages = self._get_available_pages()
        for page_key, page_info in pages.items():
            if st.button(f"{page_info['icon']} {page_info['name']}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.divider()
        
        # AI Assistant
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.session_state.current_page = 'ai_assistant'
            st.rerun()
        
        st.divider()
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.current_project = 'lead'
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    def _get_available_pages(self) -> dict:
        """Ottiene pagine disponibili per il progetto corrente"""
        base_pages = {
            'dashboard': {'name': 'Dashboard', 'icon': '📊'},
            'data_management': {'name': 'Gestione Dati', 'icon': '📋'},
            'analytics': {'name': 'Analytics', 'icon': '📈'},
            'reports': {'name': 'Report', 'icon': '📄'},
            'settings': {'name': 'Impostazioni', 'icon': '⚙️'}
        }
        
        # Aggiungi pagine specifiche per progetto
        project_specific = {
            'lead': {
                'leads': {'name': 'Lead', 'icon': '🎯'},
                'conversions': {'name': 'Conversioni', 'icon': '🔄'}
            },
            'cpa': {
                'clients': {'name': 'Clienti', 'icon': '👥'},
                'financials': {'name': 'Finanziario', 'icon': '💰'}
            },
            'prop': {
                'brokers': {'name': 'Broker', 'icon': '🏢'},
                'performance': {'name': 'Performance', 'icon': '📊'}
            }
        }
        
        # Combina pagine base con specifiche
        all_pages = {**base_pages, **project_specific.get(st.session_state.current_project, {})}
        
        return all_pages
    
    def _render_main_content(self):
        """Renderizza contenuto principale"""
        # Header
        self._render_header()
        
        # Contenuto pagina
        self._render_page_content()
    
    def _render_header(self):
        """Renderizza header"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.title(f"📊 Dashboard {st.session_state.current_project.upper()}")
        
        with col2:
            st.metric(
                "📅 Data",
                datetime.now().strftime("%d/%m/%Y")
            )
        
        with col3:
            st.metric(
                "⏰ Ora",
                datetime.now().strftime("%H:%M")
            )
        
        st.divider()
    
    def _render_page_content(self):
        """Renderizza contenuto della pagina corrente"""
        current_page = st.session_state.current_page
        current_project = st.session_state.current_project
        
        try:
            if current_page == 'dashboard':
                self._render_dashboard_page()
            elif current_page == 'data_management':
                self._render_data_management_page()
            elif current_page == 'analytics':
                self._render_analytics_page()
            elif current_page == 'reports':
                self._render_reports_page()
            elif current_page == 'ai_assistant':
                self._render_ai_assistant_page()
            elif current_page == 'settings':
                self._render_settings_page()
            else:
                # Pagine specifiche per progetto
                self._render_project_specific_page(current_page)
                
        except Exception as e:
            logger.error(f"Errore rendering pagina {current_page}: {str(e)}")
            st.error(f"❌ Errore nel caricamento della pagina: {str(e)}")
    
    def _render_dashboard_page(self):
        """Renderizza pagina dashboard"""
        st.markdown("## 📊 Panoramica Generale")
        
        # Metriche principali
        self._render_main_metrics()
        
        # Grafici principali
        self._render_main_charts()
        
        # Ultime attività
        self._render_recent_activities()
    
    def _render_main_metrics(self):
        """Renderizza metriche principali"""
        col1, col2, col3, col4 = st.columns(4)
        
        # Ottieni dati dal database corrente
        db_manager = self.db_managers[st.session_state.current_project]
        
        try:
            # Metriche base (da implementare con dati reali)
            with col1:
                st.metric(
                    "📊 Totale Record",
                    "1,234",
                    delta="+12%"
                )
            
            with col2:
                st.metric(
                    "💰 Valore Totale",
                    "€45,678",
                    delta="+8%"
                )
            
            with col3:
                st.metric(
                    "📈 Crescita",
                    "15.2%",
                    delta="+2.1%"
                )
            
            with col4:
                st.metric(
                    "🎯 Obiettivo",
                    "85%",
                    delta="+5%"
                )
                
        except Exception as e:
            logger.error(f"Errore metriche: {str(e)}")
            st.error("❌ Errore nel caricamento delle metriche")
    
    def _render_main_charts(self):
        """Renderizza grafici principali"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Trend Mensile")
            # Grafico trend (da implementare con dati reali)
            fig = px.line(
                x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
                y=[100, 120, 110, 140, 160, 150],
                title="Trend Mensile"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🥧 Distribuzione")
            # Grafico distribuzione (da implementare con dati reali)
            fig = px.pie(
                values=[30, 25, 20, 15, 10],
                names=['Categoria A', 'Categoria B', 'Categoria C', 'Categoria D', 'Categoria E'],
                title="Distribuzione per Categoria"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_recent_activities(self):
        """Renderizza attività recenti"""
        st.markdown("### 🕒 Attività Recenti")
        
        # Lista attività (da implementare con dati reali)
        activities = [
            {"time": "10:30", "action": "Nuovo lead aggiunto", "user": "Admin"},
            {"time": "09:45", "action": "Report generato", "user": "Manager"},
            {"time": "09:15", "action": "Dati aggiornati", "user": "User"},
            {"time": "08:30", "action": "Backup completato", "user": "System"},
        ]
        
        for activity in activities:
            st.markdown(f"**{activity['time']}** - {activity['action']} ({activity['user']})")
    
    def _render_data_management_page(self):
        """Renderizza pagina gestione dati"""
        st.markdown("## 📋 Gestione Dati")
        
        # Tabs per diversi tipi di dati
        tab1, tab2, tab3 = st.tabs(["📊 Visualizza", "➕ Aggiungi", "✏️ Modifica"])
        
        with tab1:
            self._render_data_view()
        
        with tab2:
            self._render_data_add()
        
        with tab3:
            self._render_data_edit()
    
    def _render_data_view(self):
        """Renderizza visualizzazione dati"""
        st.markdown("### 📊 Visualizzazione Dati")
        
        # Filtri
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_from = st.date_input("📅 Da", value=datetime.now() - timedelta(days=30))
        
        with col2:
            date_to = st.date_input("📅 A", value=datetime.now())
        
        with col3:
            if st.button("🔄 Aggiorna", use_container_width=True):
                st.rerun()
        
        # Tabella dati (da implementare con dati reali)
        st.markdown("### 📋 Dati")
        
        # Dati di esempio
        sample_data = pd.DataFrame({
            'ID': range(1, 11),
            'Nome': [f'Record {i}' for i in range(1, 11)],
            'Data': pd.date_range('2024-01-01', periods=10),
            'Valore': [100 + i * 10 for i in range(10)],
            'Stato': ['Attivo' if i % 2 == 0 else 'Inattivo' for i in range(10)]
        })
        
        st.dataframe(sample_data, use_container_width=True)
    
    def _render_data_add(self):
        """Renderizza aggiunta dati"""
        st.markdown("### ➕ Aggiungi Nuovo Record")
        
        with st.form("add_data_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome")
                data = st.date_input("Data")
            
            with col2:
                valore = st.number_input("Valore", min_value=0.0)
                stato = st.selectbox("Stato", ["Attivo", "Inattivo"])
            
            submitted = st.form_submit_button("➕ Aggiungi", use_container_width=True)
            
            if submitted:
                st.success("✅ Record aggiunto con successo!")
    
    def _render_data_edit(self):
        """Renderizza modifica dati"""
        st.markdown("### ✏️ Modifica Record")
        
        # Selezione record da modificare
        record_id = st.selectbox("Seleziona Record", options=range(1, 11))
        
        if record_id:
            with st.form("edit_data_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input("Nome", value=f"Record {record_id}")
                    data = st.date_input("Data", value=datetime.now())
                
                with col2:
                    valore = st.number_input("Valore", min_value=0.0, value=100.0)
                    stato = st.selectbox("Stato", ["Attivo", "Inattivo"])
                
                submitted = st.form_submit_button("💾 Salva Modifiche", use_container_width=True)
                
                if submitted:
                    st.success("✅ Record modificato con successo!")
    
    def _render_analytics_page(self):
        """Renderizza pagina analytics"""
        st.markdown("## 📈 Analytics Avanzate")
        
        # AI Assistant per analytics
        if st.button("🤖 Analisi AI", use_container_width=True):
            st.info("🚀 Avvio analisi AI...")
            # Implementare analisi AI
        
        # Grafici analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Performance")
            # Grafico performance
            fig = px.bar(
                x=['Q1', 'Q2', 'Q3', 'Q4'],
                y=[100, 120, 110, 140],
                title="Performance Trimestrale"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Crescita")
            # Grafico crescita
            fig = px.area(
                x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
                y=[100, 120, 110, 140, 160, 150],
                title="Crescita Mensile"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_reports_page(self):
        """Renderizza pagina report"""
        st.markdown("## 📄 Report e Esportazioni")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Genera Report")
            
            report_type = st.selectbox(
                "Tipo Report",
                ["Sintetico", "Dettagliato", "Mensile", "Trimestrale"]
            )
            
            if st.button("📄 Genera Report", use_container_width=True):
                st.success(f"✅ Report {report_type} generato!")
        
        with col2:
            st.markdown("### 📤 Esporta Dati")
            
            export_format = st.selectbox(
                "Formato Esportazione",
                ["CSV", "Excel", "PDF", "JSON"]
            )
            
            if st.button("📤 Esporta", use_container_width=True):
                st.success(f"✅ Dati esportati in formato {export_format}!")
    
    def _render_ai_assistant_page(self):
        """Renderizza pagina AI Assistant"""
        st.markdown("## 🤖 AI Assistant")
        
        # Input per l'AI
        user_question = st.text_area(
            "💬 Fai una domanda all'AI Assistant",
            placeholder="Es: Analizza le performance degli ultimi 30 giorni...",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("🚀 Analizza", use_container_width=True):
                if user_question:
                    with st.spinner("🤖 AI sta analizzando..."):
                        # Implementare chiamata AI
                        st.success("✅ Analisi completata!")
                else:
                    st.warning("⚠️ Inserisci una domanda")
        
        with col2:
            st.markdown("### 💡 Suggerimenti")
            suggestions = [
                "Analizza le performance degli ultimi 30 giorni",
                "Identifica i trend di crescita",
                "Calcola il ROI per ogni broker",
                "Genera previsioni per il prossimo mese"
            ]
            
            for suggestion in suggestions:
                if st.button(f"💡 {suggestion}", key=f"suggestion_{suggestion}"):
                    st.session_state.ai_question = suggestion
                    st.rerun()
    
    def _render_settings_page(self):
        """Renderizza pagina impostazioni"""
        st.markdown("## ⚙️ Impostazioni")
        
        tab1, tab2, tab3 = st.tabs(["🔧 Generali", "🔐 Sicurezza", "📊 Notifiche"])
        
        with tab1:
            st.markdown("### 🔧 Impostazioni Generali")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Nome Dashboard", value=self.config.app_title)
                st.text_input("Icona", value=self.config.app_icon)
            
            with col2:
                st.color_picker("Colore Tema", value=self.config.theme_color)
                st.number_input("Timeout Sessione (min)", value=60)
        
        with tab2:
            st.markdown("### 🔐 Impostazioni Sicurezza")
            
            st.checkbox("Autenticazione a due fattori")
            st.checkbox("Log delle attività")
            st.checkbox("Backup automatico")
        
        with tab3:
            st.markdown("### 📊 Impostazioni Notifiche")
            
            st.checkbox("Notifiche email")
            st.checkbox("Notifiche push")
            st.checkbox("Report automatici")
    
    def _render_project_specific_page(self, page_key: str):
        """Renderizza pagine specifiche per progetto"""
        current_project = st.session_state.current_project
        
        if current_project == 'lead' and page_key == 'leads':
            self._render_leads_page()
        elif current_project == 'lead' and page_key == 'conversions':
            self._render_conversions_page()
        elif current_project == 'cpa' and page_key == 'clients':
            self._render_clients_page()
        elif current_project == 'cpa' and page_key == 'financials':
            self._render_financials_page()
        elif current_project == 'prop' and page_key == 'brokers':
            self._render_brokers_page()
        elif current_project == 'prop' and page_key == 'performance':
            self._render_performance_page()
        else:
            st.info(f"📄 Pagina {page_key} in sviluppo...")
    
    def _render_leads_page(self):
        """Renderizza pagina lead"""
        st.markdown("## 🎯 Gestione Lead")
        st.info("📄 Pagina Lead in sviluppo...")
    
    def _render_conversions_page(self):
        """Renderizza pagina conversioni"""
        st.markdown("## 🔄 Conversioni")
        st.info("📄 Pagina Conversioni in sviluppo...")
    
    def _render_clients_page(self):
        """Renderizza pagina clienti"""
        st.markdown("## 👥 Gestione Clienti")
        st.info("📄 Pagina Clienti in sviluppo...")
    
    def _render_financials_page(self):
        """Renderizza pagina finanziario"""
        st.markdown("## 💰 Gestione Finanziaria")
        st.info("📄 Pagina Finanziario in sviluppo...")
    
    def _render_brokers_page(self):
        """Renderizza pagina broker"""
        st.markdown("## 🏢 Gestione Broker")
        st.info("📄 Pagina Broker in sviluppo...")
    
    def _render_performance_page(self):
        """Renderizza pagina performance"""
        st.markdown("## 📊 Performance")
        st.info("📄 Pagina Performance in sviluppo...")

def main():
    """Funzione principale"""
    try:
        # Inizializza e esegui dashboard
        dashboard = UnifiedDashboard()
        dashboard.run()
        
    except Exception as e:
        logger.error(f"Errore applicazione: {str(e)}")
        st.error(f"❌ Errore critico: {str(e)}")
        st.info("🔄 Ricarica la pagina per riprovare")

if __name__ == "__main__":
    main()
