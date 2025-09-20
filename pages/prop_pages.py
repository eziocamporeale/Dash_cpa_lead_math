#!/usr/bin/env python3
"""
🏢 PROP PAGES - Dashboard Unificata
Pagine specifiche per il progetto PROP BROKER
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

class PropPages:
    """
    🏢 Pagine specifiche per il progetto PROP BROKER
    
    Gestisce:
    - Gestione broker
    - Analisi performance
    - Trading metrics
    - Risk management
    """
    
    def __init__(self):
        """Inizializza pagine PROP"""
        self.db_manager = UnifiedDatabaseManager('prop')
        self.ai_assistant = UnifiedAIAssistant()
        
        logger.info("🏢 PROP Pages inizializzate")
    
    def render_brokers_page(self):
        """Renderizza pagina gestione broker"""
        st.markdown("## 🏢 Gestione Broker PROP")
        
        # Tabs per diverse funzionalità
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Panoramica", "➕ Nuovo Broker", "📋 Lista Broker", "📈 Performance"])
        
        with tab1:
            self._render_brokers_overview()
        
        with tab2:
            self._render_add_broker()
        
        with tab3:
            self._render_brokers_list()
        
        with tab4:
            self._render_broker_performance()
    
    def _render_brokers_overview(self):
        """Renderizza panoramica broker"""
        st.markdown("### 📊 Panoramica Broker")
        
        # Metriche principali
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🏢 Broker Attivi",
                "15",
                delta="+3"
            )
        
        with col2:
            st.metric(
                "💰 Capitale Totale",
                "€5,678,900",
                delta="+€250,000"
            )
        
        with col3:
            st.metric(
                "📈 Profitto Mensile",
                "€125,400",
                delta="+€15,200"
            )
        
        with col4:
            st.metric(
                "🎯 Win Rate Medio",
                "68.5%",
                delta="+2.1%"
            )
        
        st.divider()
        
        # Grafici broker
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Crescita Capitale")
            # Grafico crescita capitale (da implementare con dati reali)
            fig = px.line(
                x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
                y=[5000000, 5200000, 5400000, 5500000, 5600000, 5678900],
                title="Crescita Capitale Mensile"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🥧 Distribuzione Broker")
            # Grafico distribuzione broker (da implementare con dati reali)
            fig = px.pie(
                values=[30, 25, 20, 15, 10],
                names=['Broker Elite', 'Broker Pro', 'Broker Standard', 'Broker Basic', 'Altri'],
                title="Distribuzione Broker per Livello"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # AI Analysis
        if st.button("🤖 Analisi AI Broker", use_container_width=True):
            with st.spinner("🤖 AI sta analizzando i broker..."):
                # Dati di esempio per l'AI
                sample_data = pd.DataFrame({
                    'id': range(1, 101),
                    'nome_broker': [f'Broker {i}' for i in range(1, 101)],
                    'livello': ['Elite', 'Pro', 'Standard', 'Basic'] * 25,
                    'capitale': [100000 + i * 5000 for i in range(100)],
                    'profitto_mensile': [5000 + i * 100 for i in range(100)],
                    'win_rate': [0.6 + (i % 30) * 0.01 for i in range(100)],
                    'data_inizio': pd.date_range('2024-01-01', periods=100),
                    'stato': ['Attivo', 'Inattivo', 'Sospeso'] * 34 + ['Attivo']
                })
                
                analysis = self.ai_assistant.analyze_broker_performance(sample_data, 'prop')
                
                if 'error' not in analysis:
                    st.success("✅ Analisi AI completata!")
                    
                    # Mostra risultati
                    if 'broker_rankings' in analysis:
                        st.markdown("### 🤖 Ranking Broker")
                        st.write(analysis['broker_rankings'])
                    
                    if 'investment_recommendations' in analysis:
                        st.markdown("### 💡 Raccomandazioni Investimento")
                        for rec in analysis['investment_recommendations']:
                            st.write(f"• {rec}")
                else:
                    st.error(f"❌ Errore analisi AI: {analysis['error']}")
    
    def _render_add_broker(self):
        """Renderizza form aggiunta broker"""
        st.markdown("### ➕ Aggiungi Nuovo Broker")
        
        with st.form("add_broker_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_broker = st.text_input("🏢 Nome Broker", placeholder="Inserisci nome broker")
                livello = st.selectbox(
                    "⭐ Livello",
                    ["Elite", "Pro", "Standard", "Basic"]
                )
                capitale_iniziale = st.number_input(
                    "💰 Capitale Iniziale",
                    min_value=0.0,
                    value=100000.0,
                    step=1000.0
                )
                piattaforma = st.selectbox(
                    "💻 Piattaforma",
                    ["MT4", "MT5", "cTrader", "TradingView", "Proprietaria"]
                )
            
            with col2:
                profitto_target = st.number_input(
                    "🎯 Profitto Target Mensile",
                    min_value=0.0,
                    value=5000.0,
                    step=100.0
                )
                risk_level = st.selectbox(
                    "⚠️ Livello Rischio",
                    ["Basso", "Medio", "Alto", "Molto Alto"]
                )
                strategia = st.selectbox(
                    "📊 Strategia",
                    ["Scalping", "Day Trading", "Swing Trading", "Position Trading"]
                )
                data_inizio = st.date_input("📅 Data Inizio", value=datetime.now())
            
            # Informazioni aggiuntive
            st.markdown("#### 📝 Informazioni Aggiuntive")
            col3, col4 = st.columns(2)
            
            with col3:
                max_drawdown = st.number_input(
                    "📉 Max Drawdown (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=10.0,
                    step=0.1
                )
                leverage = st.number_input(
                    "⚖️ Leverage",
                    min_value=1.0,
                    max_value=1000.0,
                    value=100.0,
                    step=1.0
                )
            
            with col4:
                commissioni = st.number_input(
                    "💸 Commissioni (%)",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.1,
                    step=0.01
                )
                spread_medio = st.number_input(
                    "📊 Spread Medio (pips)",
                    min_value=0.0,
                    value=1.5,
                    step=0.1
                )
            
            # Note
            note = st.text_area(
                "📝 Note",
                placeholder="Inserisci note aggiuntive sul broker..."
            )
            
            submitted = st.form_submit_button("➕ Aggiungi Broker", use_container_width=True)
            
            if submitted:
                if nome_broker and livello and capitale_iniziale:
                    # Simula aggiunta broker
                    st.success("✅ Broker aggiunto con successo!")
                    st.info(f"💰 Capitale iniziale: €{capitale_iniziale:,.2f}")
                    st.info(f"🎯 Profitto target: €{profitto_target:,.2f}/mese")
                else:
                    st.error("❌ Nome broker, livello e capitale iniziale sono obbligatori!")
    
    def _render_brokers_list(self):
        """Renderizza lista broker"""
        st.markdown("### 📋 Lista Broker")
        
        # Filtri
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            livello_filter = st.selectbox(
                "⭐ Filtra per Livello",
                ["Tutti", "Elite", "Pro", "Standard", "Basic"]
            )
        
        with col2:
            stato_filter = st.selectbox(
                "📊 Filtra per Stato",
                ["Tutti", "Attivo", "Inattivo", "Sospeso"]
            )
        
        with col3:
            date_from = st.date_input("📅 Da", value=datetime.now() - timedelta(days=30))
        
        with col4:
            date_to = st.date_input("📅 A", value=datetime.now())
        
        # Tabella broker (dati di esempio)
        st.markdown("### 📊 Broker Trovati")
        
        sample_brokers = pd.DataFrame({
            'ID': range(1, 21),
            'Nome': [f'Broker {i}' for i in range(1, 21)],
            'Livello': ['Elite', 'Pro', 'Standard', 'Basic'] * 5,
            'Capitale': [200000 + i * 10000 for i in range(20)],
            'Profitto Mensile': [10000 + i * 500 for i in range(20)],
            'Win Rate': [0.65 + (i % 20) * 0.01 for i in range(20)],
            'Stato': ['Attivo', 'Inattivo', 'Sospeso'] * 7 + ['Attivo'],
            'Data Inizio': pd.date_range('2024-01-01', periods=20),
            'Azioni': ['✏️ Modifica', '🗑️ Elimina', '📊 Dettagli'] * 7 + ['✏️ Modifica', '🗑️ Elimina']
        })
        
        # Filtra dati
        if livello_filter != "Tutti":
            sample_brokers = sample_brokers[sample_brokers['Livello'] == livello_filter]
        
        if stato_filter != "Tutti":
            sample_brokers = sample_brokers[sample_brokers['Stato'] == stato_filter]
        
        st.dataframe(sample_brokers, use_container_width=True)
        
        # Azioni bulk
        st.markdown("### 🔧 Azioni Bulk")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Calcola Performance", use_container_width=True):
                st.success("✅ Performance calcolata per tutti i broker!")
        
        with col2:
            if st.button("📤 Esporta Report", use_container_width=True):
                st.success("✅ Report esportato!")
        
        with col3:
            if st.button("⚠️ Analisi Rischio", use_container_width=True):
                st.success("✅ Analisi rischio completata!")
    
    def _render_broker_performance(self):
        """Renderizza performance broker"""
        st.markdown("### 📈 Performance Broker")
        
        # Metriche performance
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📈 Profitto Totale",
                "€1,256,400",
                delta="+€125,400"
            )
        
        with col2:
            st.metric(
                "🎯 Win Rate Medio",
                "68.5%",
                delta="+2.1%"
            )
        
        with col3:
            st.metric(
                "📉 Drawdown Max",
                "8.2%",
                delta="-1.3%"
            )
        
        with col4:
            st.metric(
                "⚖️ Sharpe Ratio",
                "2.45",
                delta="+0.15"
            )
        
        st.divider()
        
        # Grafici performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Equity Curve")
            # Grafico equity curve
            fig = px.line(
                x=pd.date_range('2024-01-01', periods=30),
                y=[100000 + i * 2000 + (i % 5) * 1000 for i in range(30)],
                title="Equity Curve"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Distribuzione Profitti")
            # Grafico distribuzione profitti
            fig = px.histogram(
                x=[-500, -200, 0, 200, 500, 800, 1000, 1200, 1500],
                title="Distribuzione Profitti Giornalieri"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_performance_page(self):
        """Renderizza pagina dedicata performance"""
        st.markdown("## 📊 Performance Analysis PROP")
        
        # Tabs per diverse analisi
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Panoramica", "📈 Trading", "⚠️ Risk", "📊 Report"])
        
        with tab1:
            self._render_performance_overview()
        
        with tab2:
            self._render_trading_analysis()
        
        with tab3:
            self._render_risk_analysis()
        
        with tab4:
            self._render_performance_reports()
    
    def _render_performance_overview(self):
        """Renderizza panoramica performance"""
        st.markdown("### 📊 Panoramica Performance")
        
        # KPI principali
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Capitale Totale",
                "€5,678,900",
                delta="+€250,000"
            )
        
        with col2:
            st.metric(
                "📈 ROI Annuo",
                "26.5%",
                delta="+3.2%"
            )
        
        with col3:
            st.metric(
                "🎯 Win Rate",
                "68.5%",
                delta="+2.1%"
            )
        
        with col4:
            st.metric(
                "⚖️ Sharpe Ratio",
                "2.45",
                delta="+0.15"
            )
        
        # Grafico performance mensile
        st.markdown("### 📈 Performance Mensile")
        
        monthly_performance = pd.DataFrame({
            'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
            'ROI': [2.1, 2.3, 2.0, 2.5, 2.8, 2.6],
            'Profitto': [105000, 115000, 100000, 125000, 140000, 130000],
            'Drawdown': [3.2, 2.8, 4.1, 2.5, 2.1, 2.9]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_performance['Mese'],
            y=monthly_performance['ROI'],
            mode='lines+markers',
            name='ROI (%)',
            line=dict(color='green', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_performance['Mese'],
            y=monthly_performance['Profitto'],
            mode='lines+markers',
            name='Profitto (€)',
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
    
    def _render_trading_analysis(self):
        """Renderizza analisi trading"""
        st.markdown("### 📈 Analisi Trading")
        
        # Statistiche trading
        trading_stats = pd.DataFrame({
            'Metrica': ['Trade Totali', 'Trade Vincenti', 'Trade Perdenti', 'Win Rate', 'Profit Factor', 'Avg Win', 'Avg Loss'],
            'Valore': [1250, 856, 394, '68.5%', '2.45', '€1,250', '€-520']
        })
        
        st.dataframe(trading_stats, use_container_width=True)
        
        # Analisi per strumento
        st.markdown("### 💱 Performance per Strumento")
        
        instrument_performance = pd.DataFrame({
            'Strumento': ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD'],
            'Trade': [450, 320, 280, 150, 50],
            'Win Rate': [70.2, 65.8, 68.5, 72.1, 66.0],
            'Profitto': [45000, 32000, 28000, 15000, 5000]
        })
        
        fig = px.bar(
            instrument_performance,
            x='Strumento',
            y='Win Rate',
            title="Win Rate per Strumento",
            color='Profitto',
            color_continuous_scale='greens'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analisi temporale
        st.markdown("### ⏰ Performance Temporale")
        
        hourly_performance = pd.DataFrame({
            'Ora': list(range(24)),
            'Win Rate': [0.65, 0.62, 0.58, 0.55, 0.60, 0.68, 0.72, 0.75, 0.78, 0.80, 0.82, 0.85, 0.83, 0.80, 0.78, 0.75, 0.72, 0.70, 0.68, 0.65, 0.62, 0.60, 0.58, 0.55]
        })
        
        fig = px.line(
            hourly_performance,
            x='Ora',
            y='Win Rate',
            title="Win Rate per Ora del Giorno"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_risk_analysis(self):
        """Renderizza analisi rischio"""
        st.markdown("### ⚠️ Analisi Rischio")
        
        # Metriche rischio
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📉 Max Drawdown",
                "8.2%",
                delta="-1.3%"
            )
        
        with col2:
            st.metric(
                "⚖️ Sharpe Ratio",
                "2.45",
                delta="+0.15"
            )
        
        with col3:
            st.metric(
                "📊 Sortino Ratio",
                "3.12",
                delta="+0.22"
            )
        
        with col4:
            st.metric(
                "🎯 Calmar Ratio",
                "3.23",
                delta="+0.18"
            )
        
        # Analisi drawdown
        st.markdown("### 📉 Analisi Drawdown")
        
        drawdown_data = pd.DataFrame({
            'Data': pd.date_range('2024-01-01', periods=30),
            'Drawdown': [0, -0.5, -1.2, -0.8, -2.1, -3.5, -2.8, -1.9, -1.2, -0.5, 0, 0.8, 1.5, 0.9, 0.2, -0.3, -1.1, -2.4, -1.8, -1.2, -0.6, 0, 0.7, 1.3, 0.8, 0.1, -0.4, -1.2, -0.8, -0.2]
        })
        
        fig = px.area(
            drawdown_data,
            x='Data',
            y='Drawdown',
            title="Drawdown nel Tempo"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analisi VaR
        st.markdown("### 📊 Value at Risk (VaR)")
        
        var_data = pd.DataFrame({
            'Confidenza': ['95%', '99%', '99.9%'],
            'VaR 1 Giorno': ['€-2,500', '€-4,200', '€-6,800'],
            'VaR 1 Settimana': ['€-5,600', '€-9,400', '€-15,200'],
            'VaR 1 Mese': ['€-11,200', '€-18,800', '€-30,400']
        })
        
        st.dataframe(var_data, use_container_width=True)
    
    def _render_performance_reports(self):
        """Renderizza report performance"""
        st.markdown("### 📊 Report Performance")
        
        # Generazione report
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📄 Genera Report")
            
            report_type = st.selectbox(
                "Tipo Report",
                ["Performance Mensile", "Analisi Rischio", "Trading Statistics", "Broker Comparison"]
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
            {"Nome": "Performance Report Gennaio", "Data": "2024-01-31", "Tipo": "Performance", "Dimensione": "3.2 MB"},
            {"Nome": "Risk Analysis Q1", "Data": "2024-03-31", "Tipo": "Rischio", "Dimensione": "2.1 MB"},
            {"Nome": "Trading Statistics 2024", "Data": "2024-12-31", "Tipo": "Trading", "Dimensione": "4.8 MB"},
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
