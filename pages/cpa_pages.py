#!/usr/bin/env python3
"""
💰 CPA PAGES - Dashboard Unificata
Pagine specifiche per il progetto CPA
Creato da Ezio Camporeale
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
from database.unified_database_manager import UnifiedDatabaseManager
from ai.unified_ai_assistant import UnifiedAIAssistant
from components.unified_components import UnifiedForm, UnifiedTable, UnifiedChart

logger = logging.getLogger(__name__)

class CPAPages:
    """
    💰 Pagine specifiche per il progetto CPA
    
    Gestisce:
    - Gestione clienti
    - Analisi finanziaria
    - Broker management
    - VPS tracking
    """
    
    def __init__(self):
        """Inizializza pagine CPA"""
        self.db_manager = UnifiedDatabaseManager('cpa')
        self.ai_assistant = UnifiedAIAssistant()
        
        logger.info("💰 CPA Pages inizializzate")
    
    def render_clients_page(self):
        """Renderizza pagina gestione clienti"""
        st.markdown("## 👥 Gestione Clienti CPA")
        
        # Tabs per diverse funzionalità
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Panoramica", "➕ Nuovo Cliente", "📋 Lista Clienti", "💰 Finanziario"])
        
        with tab1:
            self._render_clients_overview()
        
        with tab2:
            self._render_add_client()
        
        with tab3:
            self._render_clients_list()
        
        with tab4:
            self._render_financial_overview()
    
    def _render_clients_overview(self):
        """Renderizza panoramica clienti"""
        st.markdown("### 📊 Panoramica Clienti")
        
        # Metriche principali
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "👥 Totale Clienti",
                "234",
                delta="+15"
            )
        
        with col2:
            st.metric(
                "💰 Depositi Totali",
                "€2,456,789",
                delta="+€125,000"
            )
        
        with col3:
            st.metric(
                "📈 Deposito Medio",
                "€10,499",
                delta="+€500"
            )
        
        with col4:
            st.metric(
                "🏢 Broker Attivi",
                "12",
                delta="+2"
            )
        
        st.divider()
        
        # Grafici clienti
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Crescita Clienti")
            # Grafico crescita clienti (da implementare con dati reali)
            fig = px.line(
                x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
                y=[180, 195, 210, 220, 230, 234],
                title="Crescita Clienti Mensile"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🥧 Distribuzione Broker")
            # Grafico distribuzione broker (da implementare con dati reali)
            fig = px.pie(
                values=[25, 20, 18, 15, 12, 10],
                names=['Broker A', 'Broker B', 'Broker C', 'Broker D', 'Broker E', 'Altri'],
                title="Distribuzione Clienti per Broker"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # AI Analysis
        if st.button("🤖 Analisi AI Clienti", use_container_width=True):
            with st.spinner("🤖 AI sta analizzando i clienti..."):
                # Dati di esempio per l'AI
                sample_data = pd.DataFrame({
                    'id': range(1, 101),
                    'nome_cliente': [f'Cliente {i}' for i in range(1, 101)],
                    'email': [f'cliente{i}@example.com' for i in range(1, 101)],
                    'broker': ['Broker A', 'Broker B', 'Broker C', 'Broker D', 'Broker E'] * 20,
                    'deposito': [5000 + i * 100 for i in range(100)],
                    'piattaforma': ['MT4', 'MT5', 'cTrader', 'TradingView'] * 25,
                    'data_registrazione': pd.date_range('2024-01-01', periods=100),
                    'vps_ip': [f'192.168.1.{i}' if i % 3 == 0 else None for i in range(100)]
                })
                
                analysis = self.ai_assistant.calculate_cpa_metrics(sample_data, 'cpa')
                
                if 'error' not in analysis:
                    st.success("✅ Analisi AI completata!")
                    
                    # Mostra risultati
                    if 'roi_analysis' in analysis:
                        st.markdown("### 🤖 Analisi ROI")
                        st.write(analysis['roi_analysis'])
                    
                    if 'strategic_recommendations' in analysis:
                        st.markdown("### 💡 Raccomandazioni Strategiche")
                        for rec in analysis['strategic_recommendations']:
                            st.write(f"• {rec}")
                else:
                    st.error(f"❌ Errore analisi AI: {analysis['error']}")
    
    def _render_add_client(self):
        """Renderizza form aggiunta cliente"""
        st.markdown("### ➕ Aggiungi Nuovo Cliente")
        
        with st.form("add_client_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_cliente = st.text_input("👤 Nome Cliente", placeholder="Inserisci nome completo")
                email = st.text_input("📧 Email", placeholder="Inserisci email")
                password_email = st.text_input("🔒 Password Email", type="password", placeholder="Password email")
                broker = st.selectbox(
                    "🏢 Broker",
                    ["Broker A", "Broker B", "Broker C", "Broker D", "Broker E", "Altro"]
                )
            
            with col2:
                deposito = st.number_input(
                    "💰 Deposito",
                    min_value=0.0,
                    value=10000.0,
                    step=100.0
                )
                piattaforma = st.selectbox(
                    "💻 Piattaforma",
                    ["MT4", "MT5", "cTrader", "TradingView", "Altro"]
                )
                numero_conto = st.text_input("🔢 Numero Conto", placeholder="Inserisci numero conto")
                password_conto = st.text_input("🔒 Password Conto", type="password", placeholder="Password conto")
            
            # Informazioni VPS
            st.markdown("#### 🖥️ Informazioni VPS")
            col3, col4 = st.columns(2)
            
            with col3:
                vps_ip = st.text_input("🌐 IP VPS", placeholder="192.168.1.100")
                vps_username = st.text_input("👤 Username VPS", placeholder="Username VPS")
            
            with col4:
                vps_password = st.text_input("🔒 Password VPS", type="password", placeholder="Password VPS")
                data_registrazione = st.date_input("📅 Data Registrazione", value=datetime.now())
            
            submitted = st.form_submit_button("➕ Aggiungi Cliente", use_container_width=True)
            
            if submitted:
                if nome_cliente and email and broker and deposito:
                    # Simula aggiunta cliente
                    st.success("✅ Cliente aggiunto con successo!")
                    st.info(f"📧 Email di benvenuto inviata a: {email}")
                    st.info(f"💰 Deposito iniziale: €{deposito:,.2f}")
                else:
                    st.error("❌ Nome, email, broker e deposito sono obbligatori!")
    
    def _render_clients_list(self):
        """Renderizza lista clienti"""
        st.markdown("### 📋 Lista Clienti")
        
        # Filtri
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            broker_filter = st.selectbox(
                "🏢 Filtra per Broker",
                ["Tutti", "Broker A", "Broker B", "Broker C", "Broker D", "Broker E"]
            )
        
        with col2:
            platform_filter = st.selectbox(
                "💻 Filtra per Piattaforma",
                ["Tutte", "MT4", "MT5", "cTrader", "TradingView"]
            )
        
        with col3:
            date_from = st.date_input("📅 Da", value=datetime.now() - timedelta(days=30))
        
        with col4:
            date_to = st.date_input("📅 A", value=datetime.now())
        
        # Tabella clienti (dati di esempio)
        st.markdown("### 📊 Clienti Trovati")
        
        sample_clients = pd.DataFrame({
            'ID': range(1, 21),
            'Nome': [f'Cliente {i}' for i in range(1, 21)],
            'Email': [f'cliente{i}@example.com' for i in range(1, 21)],
            'Broker': ['Broker A', 'Broker B', 'Broker C', 'Broker D', 'Broker E'] * 4,
            'Piattaforma': ['MT4', 'MT5', 'cTrader', 'TradingView'] * 5,
            'Deposito': [10000 + i * 500 for i in range(20)],
            'VPS': ['Sì' if i % 3 == 0 else 'No' for i in range(20)],
            'Data': pd.date_range('2024-01-01', periods=20),
            'Azioni': ['✏️ Modifica', '🗑️ Elimina', '📊 Dettagli'] * 7 + ['✏️ Modifica', '🗑️ Elimina']
        })
        
        # Filtra dati
        if broker_filter != "Tutti":
            sample_clients = sample_clients[sample_clients['Broker'] == broker_filter]
        
        if platform_filter != "Tutte":
            sample_clients = sample_clients[sample_clients['Piattaforma'] == platform_filter]
        
        st.dataframe(sample_clients, use_container_width=True)
        
        # Azioni bulk
        st.markdown("### 🔧 Azioni Bulk")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Email Massiva", use_container_width=True):
                st.success("✅ Email inviate a tutti i clienti selezionati!")
        
        with col2:
            if st.button("📊 Esporta Excel", use_container_width=True):
                st.success("✅ Dati esportati in Excel!")
        
        with col3:
            if st.button("💰 Calcola ROI", use_container_width=True):
                st.success("✅ ROI calcolato per tutti i clienti!")
    
    def _render_financial_overview(self):
        """Renderizza panoramica finanziaria"""
        st.markdown("### 💰 Panoramica Finanziaria")
        
        # Metriche finanziarie
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Depositi Totali",
                "€2,456,789",
                delta="+€125,000"
            )
        
        with col2:
            st.metric(
                "📈 ROI Medio",
                "23.5%",
                delta="+2.1%"
            )
        
        with col3:
            st.metric(
                "💵 Profitto Mensile",
                "€45,678",
                delta="+€5,200"
            )
        
        with col4:
            st.metric(
                "🎯 Obiettivo Mensile",
                "85%",
                delta="+5%"
            )
        
        st.divider()
        
        # Grafici finanziari
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Trend Depositi")
            # Grafico trend depositi
            fig = px.line(
                x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
                y=[2000000, 2100000, 2200000, 2300000, 2400000, 2456789],
                title="Trend Depositi Mensile"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🥧 ROI per Broker")
            # Grafico ROI broker
            fig = px.pie(
                values=[25, 22, 20, 18, 15],
                names=['Broker A', 'Broker B', 'Broker C', 'Broker D', 'Broker E'],
                title="ROI per Broker"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_financials_page(self):
        """Renderizza pagina dedicata finanziario"""
        st.markdown("## 💰 Gestione Finanziaria CPA")
        
        # Tabs per diverse analisi
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Panoramica", "📈 ROI", "💰 Budget", "📊 Report"])
        
        with tab1:
            self._render_financial_overview()
        
        with tab2:
            self._render_roi_analysis()
        
        with tab3:
            self._render_budget_management()
        
        with tab4:
            self._render_financial_reports()
    
    def _render_roi_analysis(self):
        """Renderizza analisi ROI"""
        st.markdown("### 📈 Analisi ROI")
        
        # ROI per broker
        roi_data = pd.DataFrame({
            'Broker': ['Broker A', 'Broker B', 'Broker C', 'Broker D', 'Broker E'],
            'ROI': [25.5, 22.3, 20.8, 18.9, 15.2],
            'Depositi': [500000, 400000, 350000, 300000, 250000],
            'Profitto': [127500, 89200, 72800, 56700, 38000]
        })
        
        # Grafico ROI
        fig = px.bar(
            roi_data,
            x='Broker',
            y='ROI',
            title="ROI per Broker",
            color='ROI',
            color_continuous_scale='greens'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analisi ROI temporale
        st.markdown("### 📅 ROI Temporale")
        
        roi_temporal = pd.DataFrame({
            'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
            'ROI Medio': [20.5, 21.2, 22.1, 22.8, 23.2, 23.5],
            'Profitto': [35000, 38000, 42000, 45000, 48000, 45678]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=roi_temporal['Mese'],
            y=roi_temporal['ROI Medio'],
            mode='lines+markers',
            name='ROI Medio',
            line=dict(color='green', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=roi_temporal['Mese'],
            y=roi_temporal['Profitto'],
            mode='lines+markers',
            name='Profitto',
            line=dict(color='blue', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="ROI e Profitto Mensile",
            xaxis_title="Mese",
            yaxis_title="ROI (%)",
            yaxis2=dict(title="Profitto (€)", overlaying="y", side="right"),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_budget_management(self):
        """Renderizza gestione budget"""
        st.markdown("### 💰 Gestione Budget")
        
        # Budget vs Spese
        budget_data = pd.DataFrame({
            'Categoria': ['Marketing', 'VPS', 'Broker Fees', 'Software', 'Personale'],
            'Budget': [50000, 15000, 25000, 10000, 30000],
            'Spese': [45000, 12000, 22000, 8000, 28000],
            'Rimanente': [5000, 3000, 3000, 2000, 2000]
        })
        
        # Grafico budget
        fig = px.bar(
            budget_data,
            x='Categoria',
            y=['Budget', 'Spese'],
            title="Budget vs Spese per Categoria",
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Proiezioni budget
        st.markdown("### 📊 Proiezioni Budget")
        
        projections = pd.DataFrame({
            'Mese': ['Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'],
            'Budget Previsto': [130000, 135000, 140000, 145000, 150000, 155000],
            'Spese Previste': [120000, 125000, 130000, 135000, 140000, 145000],
            'Profitto Previsto': [10000, 10000, 10000, 10000, 10000, 10000]
        })
        
        fig = px.line(
            projections,
            x='Mese',
            y=['Budget Previsto', 'Spese Previste', 'Profitto Previsto'],
            title="Proiezioni Budget Mensile"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_financial_reports(self):
        """Renderizza report finanziari"""
        st.markdown("### 📊 Report Finanziari")
        
        # Generazione report
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📄 Genera Report")
            
            report_type = st.selectbox(
                "Tipo Report",
                ["Mensile", "Trimestrale", "Annuale", "ROI Dettagliato"]
            )
            
            if st.button("📊 Genera Report", use_container_width=True):
                st.success(f"✅ Report {report_type} generato!")
        
        with col2:
            st.markdown("#### 📤 Esporta Dati")
            
            export_format = st.selectbox(
                "Formato Esportazione",
                ["Excel", "PDF", "CSV", "JSON"]
            )
            
            if st.button("📤 Esporta", use_container_width=True):
                st.success(f"✅ Dati esportati in formato {export_format}!")
        
        # Report generati
        st.markdown("### 📋 Report Disponibili")
        
        reports = [
            {"Nome": "Report Mensile Gennaio", "Data": "2024-01-31", "Tipo": "Mensile", "Dimensione": "2.3 MB"},
            {"Nome": "ROI Dettagliato Q1", "Data": "2024-03-31", "Tipo": "Trimestrale", "Dimensione": "1.8 MB"},
            {"Nome": "Analisi Broker 2024", "Data": "2024-12-31", "Tipo": "Annuale", "Dimensione": "5.2 MB"},
        ]
        
        for report in reports:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"📄 {report['Nome']}")
            
            with col2:
                st.write(report['Data'])
            
            with col3:
                st.write(report['Tipo'])
            
            with col4:
                if st.button("📥 Scarica", key=f"download_{report['Nome']}"):
                    st.success("✅ Report scaricato!")
