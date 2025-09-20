#!/usr/bin/env python3
"""
🎯 LEAD PAGES - Dashboard Unificata
Pagine specifiche per il progetto LEAD
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

class LeadPages:
    """
    🎯 Pagine specifiche per il progetto LEAD
    
    Gestisce:
    - Lead management
    - Conversioni
    - Analytics lead
    - Report lead
    """
    
    def __init__(self):
        """Inizializza pagine LEAD"""
        self.db_manager = UnifiedDatabaseManager('lead')
        self.ai_assistant = UnifiedAIAssistant()
        
        logger.info("🎯 Lead Pages inizializzate")
    
    def render_leads_page(self):
        """Renderizza pagina gestione lead"""
        st.markdown("## 🎯 Gestione Lead")
        
        # Tabs per diverse funzionalità
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Panoramica", "➕ Nuovo Lead", "📋 Lista Lead", "🔄 Conversioni"])
        
        with tab1:
            self._render_leads_overview()
        
        with tab2:
            self._render_add_lead()
        
        with tab3:
            self._render_leads_list()
        
        with tab4:
            self._render_conversions()
    
    def _render_leads_overview(self):
        """Renderizza panoramica lead"""
        st.markdown("### 📊 Panoramica Lead")
        
        # Metriche principali
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🎯 Totale Lead",
                "1,234",
                delta="+12%"
            )
        
        with col2:
            st.metric(
                "✅ Convertiti",
                "456",
                delta="+8%"
            )
        
        with col3:
            st.metric(
                "📈 Tasso Conversione",
                "37%",
                delta="+2.1%"
            )
        
        with col4:
            st.metric(
                "💰 Valore Totale",
                "€45,678",
                delta="+15%"
            )
        
        st.divider()
        
        # Grafici lead
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Trend Lead")
            # Grafico trend lead (da implementare con dati reali)
            fig = px.line(
                x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
                y=[100, 120, 110, 140, 160, 150],
                title="Trend Lead Mensile"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🥧 Fonti Lead")
            # Grafico fonti lead (da implementare con dati reali)
            fig = px.pie(
                values=[30, 25, 20, 15, 10],
                names=['Google', 'Facebook', 'LinkedIn', 'Email', 'Altro'],
                title="Distribuzione per Fonte"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # AI Analysis
        if st.button("🤖 Analisi AI Lead", use_container_width=True):
            with st.spinner("🤖 AI sta analizzando i lead..."):
                # Dati di esempio per l'AI
                sample_data = pd.DataFrame({
                    'id': range(1, 101),
                    'nome': [f'Lead {i}' for i in range(1, 101)],
                    'email': [f'lead{i}@example.com' for i in range(1, 101)],
                    'fonte': ['Google', 'Facebook', 'LinkedIn', 'Email', 'Altro'] * 20,
                    'stato': ['nuovo', 'contattato', 'qualificato', 'converted', 'lost'] * 20,
                    'data_registrazione': pd.date_range('2024-01-01', periods=100),
                    'valore_stimato': [100 + i * 10 for i in range(100)]
                })
                
                analysis = self.ai_assistant.analyze_lead_data(sample_data, 'lead')
                
                if 'error' not in analysis:
                    st.success("✅ Analisi AI completata!")
                    
                    # Mostra risultati
                    if 'analysis' in analysis:
                        st.markdown("### 🤖 Analisi AI")
                        st.write(analysis['analysis'])
                    
                    if 'recommendations' in analysis:
                        st.markdown("### 💡 Raccomandazioni")
                        for rec in analysis['recommendations']:
                            st.write(f"• {rec}")
                else:
                    st.error(f"❌ Errore analisi AI: {analysis['error']}")
    
    def _render_add_lead(self):
        """Renderizza form aggiunta lead"""
        st.markdown("### ➕ Aggiungi Nuovo Lead")
        
        with st.form("add_lead_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("👤 Nome Completo", placeholder="Inserisci nome completo")
                email = st.text_input("📧 Email", placeholder="Inserisci email")
                telefono = st.text_input("📞 Telefono", placeholder="Inserisci telefono")
            
            with col2:
                fonte = st.selectbox(
                    "📡 Fonte",
                    ["Google", "Facebook", "LinkedIn", "Email", "Referral", "Altro"]
                )
                stato = st.selectbox(
                    "📊 Stato",
                    ["Nuovo", "Contattato", "Qualificato", "Convertito", "Perso"]
                )
                valore_stimato = st.number_input(
                    "💰 Valore Stimato",
                    min_value=0.0,
                    value=1000.0,
                    step=100.0
                )
            
            # Note aggiuntive
            note = st.text_area(
                "📝 Note",
                placeholder="Inserisci note aggiuntive sul lead..."
            )
            
            submitted = st.form_submit_button("➕ Aggiungi Lead", use_container_width=True)
            
            if submitted:
                if nome and email:
                    # Simula aggiunta lead
                    st.success("✅ Lead aggiunto con successo!")
                    st.info(f"📧 Email di benvenuto inviata a: {email}")
                else:
                    st.error("❌ Nome ed email sono obbligatori!")
    
    def _render_leads_list(self):
        """Renderizza lista lead"""
        st.markdown("### 📋 Lista Lead")
        
        # Filtri
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            stato_filter = st.selectbox(
                "📊 Filtra per Stato",
                ["Tutti", "Nuovo", "Contattato", "Qualificato", "Convertito", "Perso"]
            )
        
        with col2:
            fonte_filter = st.selectbox(
                "📡 Filtra per Fonte",
                ["Tutte", "Google", "Facebook", "LinkedIn", "Email", "Referral", "Altro"]
            )
        
        with col3:
            date_from = st.date_input("📅 Da", value=datetime.now() - timedelta(days=30))
        
        with col4:
            date_to = st.date_input("📅 A", value=datetime.now())
        
        # Tabella lead (dati di esempio)
        st.markdown("### 📊 Lead Trovati")
        
        sample_leads = pd.DataFrame({
            'ID': range(1, 21),
            'Nome': [f'Lead {i}' for i in range(1, 21)],
            'Email': [f'lead{i}@example.com' for i in range(1, 21)],
            'Telefono': [f'+39 123 456 789{i:02d}' for i in range(1, 21)],
            'Fonte': ['Google', 'Facebook', 'LinkedIn', 'Email', 'Referral'] * 4,
            'Stato': ['Nuovo', 'Contattato', 'Qualificato', 'Convertito', 'Perso'] * 4,
            'Valore': [1000 + i * 100 for i in range(20)],
            'Data': pd.date_range('2024-01-01', periods=20),
            'Azioni': ['✏️ Modifica', '🗑️ Elimina', '📧 Contatta'] * 7 + ['✏️ Modifica', '🗑️ Elimina']
        })
        
        # Filtra dati
        if stato_filter != "Tutti":
            sample_leads = sample_leads[sample_leads['Stato'] == stato_filter]
        
        if fonte_filter != "Tutte":
            sample_leads = sample_leads[sample_leads['Fonte'] == fonte_filter]
        
        st.dataframe(sample_leads, use_container_width=True)
        
        # Azioni bulk
        st.markdown("### 🔧 Azioni Bulk")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Invia Email Massiva", use_container_width=True):
                st.success("✅ Email inviate a tutti i lead selezionati!")
        
        with col2:
            if st.button("📊 Esporta CSV", use_container_width=True):
                st.success("✅ Dati esportati in CSV!")
        
        with col3:
            if st.button("🗑️ Elimina Selezionati", use_container_width=True):
                st.warning("⚠️ Conferma eliminazione lead selezionati")
    
    def _render_conversions(self):
        """Renderizza pagina conversioni"""
        st.markdown("### 🔄 Analisi Conversioni")
        
        # Metriche conversioni
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🔄 Tasso Conversione",
                "37.2%",
                delta="+2.1%"
            )
        
        with col2:
            st.metric(
                "⏱️ Tempo Medio Conversione",
                "12.5 giorni",
                delta="-1.2 giorni"
            )
        
        with col3:
            st.metric(
                "💰 Valore Medio Conversione",
                "€2,450",
                delta="+€150"
            )
        
        st.divider()
        
        # Funnel conversioni
        st.markdown("### 🎯 Funnel Conversioni")
        
        funnel_data = {
            'Fase': ['Lead Iniziali', 'Contattati', 'Qualificati', 'Convertiti'],
            'Numero': [1000, 750, 450, 167],
            'Percentuale': [100, 75, 45, 16.7]
        }
        
        fig = px.funnel(
            funnel_data,
            x='Numero',
            y='Fase',
            title="Funnel di Conversione"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analisi per fonte
        st.markdown("### 📊 Conversioni per Fonte")
        
        source_conversion = pd.DataFrame({
            'Fonte': ['Google', 'Facebook', 'LinkedIn', 'Email', 'Referral'],
            'Lead Totali': [300, 250, 200, 150, 100],
            'Convertiti': [120, 95, 80, 60, 45],
            'Tasso Conversione': [40, 38, 40, 40, 45]
        })
        
        fig = px.bar(
            source_conversion,
            x='Fonte',
            y='Tasso Conversione',
            title="Tasso Conversione per Fonte",
            color='Tasso Conversione',
            color_continuous_scale='viridis'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_conversions_page(self):
        """Renderizza pagina dedicata conversioni"""
        st.markdown("## 🔄 Gestione Conversioni")
        
        # Tabs per diverse analisi
        tab1, tab2, tab3 = st.tabs(["📊 Panoramica", "🎯 Funnel", "📈 Trend"])
        
        with tab1:
            self._render_conversions_overview()
        
        with tab2:
            self._render_conversion_funnel()
        
        with tab3:
            self._render_conversion_trends()
    
    def _render_conversions_overview(self):
        """Renderizza panoramica conversioni"""
        st.markdown("### 📊 Panoramica Conversioni")
        
        # KPI principali
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🎯 Conversioni Totali",
                "456",
                delta="+23"
            )
        
        with col2:
            st.metric(
                "📈 Tasso Conversione",
                "37.2%",
                delta="+2.1%"
            )
        
        with col3:
            st.metric(
                "💰 Valore Totale",
                "€1,117,200",
                delta="+€45,000"
            )
        
        with col4:
            st.metric(
                "⏱️ Tempo Medio",
                "12.5 giorni",
                delta="-1.2 giorni"
            )
        
        # Grafico conversioni mensili
        st.markdown("### 📈 Conversioni Mensili")
        
        monthly_conversions = pd.DataFrame({
            'Mese': ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
            'Conversioni': [35, 42, 38, 45, 52, 48],
            'Valore': [87500, 105000, 95000, 112500, 130000, 120000]
        })
        
        fig = px.bar(
            monthly_conversions,
            x='Mese',
            y='Conversioni',
            title="Conversioni per Mese",
            color='Valore',
            color_continuous_scale='blues'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_conversion_funnel(self):
        """Renderizza funnel conversioni"""
        st.markdown("### 🎯 Funnel di Conversione")
        
        # Dati funnel
        funnel_stages = {
            'Fase': ['Visite', 'Lead', 'Contattati', 'Qualificati', 'Convertiti'],
            'Numero': [10000, 1000, 750, 450, 167],
            'Percentuale': [100, 10, 7.5, 4.5, 1.67]
        }
        
        # Grafico funnel
        fig = px.funnel(
            funnel_stages,
            x='Numero',
            y='Fase',
            title="Funnel Completo di Conversione"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analisi perdite
        st.markdown("### 📉 Analisi Perdite")
        
        loss_analysis = pd.DataFrame({
            'Fase': ['Lead → Contattati', 'Contattati → Qualificati', 'Qualificati → Convertiti'],
            'Perdite': [250, 300, 283],
            'Percentuale Perdita': [25, 40, 63]
        })
        
        fig = px.bar(
            loss_analysis,
            x='Fase',
            y='Percentuale Perdita',
            title="Percentuale di Perdita per Fase",
            color='Percentuale Perdita',
            color_continuous_scale='reds'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_conversion_trends(self):
        """Renderizza trend conversioni"""
        st.markdown("### 📈 Trend Conversioni")
        
        # Trend temporali
        trend_data = pd.DataFrame({
            'Data': pd.date_range('2024-01-01', periods=30),
            'Conversioni': [2, 3, 1, 4, 2, 5, 3, 4, 6, 5, 7, 4, 6, 8, 5, 7, 9, 6, 8, 7, 9, 8, 10, 7, 9, 11, 8, 10, 9, 11],
            'Lead': [10, 12, 8, 15, 11, 18, 13, 16, 20, 17, 22, 15, 19, 25, 18, 22, 28, 20, 25, 23, 27, 24, 30, 21, 26, 32, 23, 28, 25, 30]
        })
        
        # Grafico trend
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend_data['Data'],
            y=trend_data['Conversioni'],
            mode='lines+markers',
            name='Conversioni',
            line=dict(color='green', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=trend_data['Data'],
            y=trend_data['Lead'],
            mode='lines+markers',
            name='Lead Totali',
            line=dict(color='blue', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Trend Conversioni vs Lead",
            xaxis_title="Data",
            yaxis_title="Conversioni",
            yaxis2=dict(title="Lead Totali", overlaying="y", side="right"),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analisi stagionalità
        st.markdown("### 📅 Analisi Stagionalità")
        
        seasonal_data = pd.DataFrame({
            'Giorno Settimana': ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'],
            'Conversioni': [15, 18, 20, 22, 25, 12, 8],
            'Lead': [45, 52, 58, 63, 70, 35, 25]
        })
        
        fig = px.bar(
            seasonal_data,
            x='Giorno Settimana',
            y='Conversioni',
            title="Conversioni per Giorno della Settimana",
            color='Conversioni',
            color_continuous_scale='greens'
        )
        
        st.plotly_chart(fig, use_container_width=True)
