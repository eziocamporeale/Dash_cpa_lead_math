#!/usr/bin/env python3
"""
🎨 COMPONENTI UI UNIFICATI - Dashboard Unificata
Componenti riutilizzabili per tutti e 3 i progetti
Basati sui migliori elementi di DASH_GESTIONE_LEAD
Creato da Ezio Camporeale
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, date
import json

# Import configurazione e database
from config import get_app_config
from database import get_database_manager
from auth import get_current_project, get_current_user

class UnifiedForm:
    """Form unificato per tutti i progetti"""
    
    def __init__(self, form_type: str, project_type: str = None):
        """
        Inizializza form unificato
        
        Args:
            form_type: Tipo di form ('lead', 'client', 'broker', etc.)
            project_type: Tipo di progetto ('lead', 'cpa', 'prop')
        """
        self.form_type = form_type
        self.project_type = project_type or get_current_project()
        self.db_manager = get_database_manager(self.project_type)
        self.app_config = get_app_config()
        
        # Configurazioni form per tipo
        self.form_configs = self._init_form_configs()
    
    def _init_form_configs(self) -> Dict[str, Dict[str, Any]]:
        """Inizializza configurazioni form per tipo"""
        return {
            'lead': {
                'title': '🎯 Nuovo Lead',
                'fields': [
                    {'name': 'name', 'label': 'Nome Lead', 'type': 'text', 'required': True},
                    {'name': 'email', 'label': 'Email', 'type': 'email', 'required': False},
                    {'name': 'phone', 'label': 'Telefono', 'type': 'text', 'required': False},
                    {'name': 'company', 'label': 'Azienda', 'type': 'text', 'required': False},
                    {'name': 'position', 'label': 'Posizione', 'type': 'text', 'required': False},
                    {'name': 'budget', 'label': 'Budget', 'type': 'number', 'required': False},
                    {'name': 'expected_close_date', 'label': 'Data Chiusura Prevista', 'type': 'date', 'required': False},
                    {'name': 'notes', 'label': 'Note', 'type': 'textarea', 'required': False}
                ],
                'table': 'leads'
            },
            'client': {
                'title': '💼 Nuovo Cliente CPA',
                'fields': [
                    {'name': 'nome_cliente', 'label': 'Nome Cliente', 'type': 'text', 'required': True},
                    {'name': 'email', 'label': 'Email', 'type': 'email', 'required': True},
                    {'name': 'password_email', 'label': 'Password Email', 'type': 'password', 'required': False},
                    {'name': 'broker', 'label': 'Broker', 'type': 'text', 'required': True},
                    {'name': 'data_registrazione', 'label': 'Data Registrazione', 'type': 'date', 'required': True},
                    {'name': 'deposito', 'label': 'Deposito', 'type': 'number', 'required': True},
                    {'name': 'piattaforma', 'label': 'Piattaforma', 'type': 'select', 'required': True, 'options': ['MT4', 'MT5', 'cTrader', 'Altro']},
                    {'name': 'numero_conto', 'label': 'Numero Conto', 'type': 'text', 'required': True},
                    {'name': 'password_conto', 'label': 'Password Conto', 'type': 'password', 'required': False},
                    {'name': 'vps_ip', 'label': 'VPS IP', 'type': 'text', 'required': False},
                    {'name': 'vps_username', 'label': 'VPS Username', 'type': 'text', 'required': False},
                    {'name': 'vps_password', 'label': 'VPS Password', 'type': 'password', 'required': False}
                ],
                'table': 'clienti'
            },
            'broker': {
                'title': '🧮 Nuovo Broker',
                'fields': [
                    {'name': 'nome_broker', 'label': 'Nome Broker', 'type': 'text', 'required': True},
                    {'name': 'tipo_broker', 'label': 'Tipo Broker', 'type': 'select', 'required': False, 'options': ['ECN', 'STP', 'Market Maker']},
                    {'name': 'regolamentazione', 'label': 'Regolamentazione', 'type': 'text', 'required': False},
                    {'name': 'paese', 'label': 'Paese', 'type': 'text', 'required': False},
                    {'name': 'sito_web', 'label': 'Sito Web', 'type': 'url', 'required': False},
                    {'name': 'spread_minimo', 'label': 'Spread Minimo', 'type': 'number', 'required': False, 'step': 0.00001},
                    {'name': 'commissioni', 'label': 'Commissioni', 'type': 'number', 'required': False, 'step': 0.00001},
                    {'name': 'leverage_massimo', 'label': 'Leverage Massimo', 'type': 'number', 'required': False},
                    {'name': 'deposito_minimo', 'label': 'Deposito Minimo', 'type': 'number', 'required': False, 'step': 0.01},
                    {'name': 'valute_supportate', 'label': 'Valute Supportate', 'type': 'text', 'required': False},
                    {'name': 'piattaforme', 'label': 'Piattaforme', 'type': 'text', 'required': False},
                    {'name': 'note', 'label': 'Note', 'type': 'textarea', 'required': False}
                ],
                'table': 'brokers'
            }
        }
    
    def render_form(self, edit_data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Rende il form"""
        config = self.form_configs.get(self.form_type, {})
        if not config:
            st.error(f"❌ Tipo form non supportato: {self.form_type}")
            return None
        
        st.markdown(f"### {config['title']}")
        
        with st.form(f"{self.form_type}_form"):
            form_data = {}
            
            for field in config['fields']:
                field_name = field['name']
                field_label = field['label']
                field_type = field['type']
                field_required = field.get('required', False)
                field_value = edit_data.get(field_name, '') if edit_data else ''
                
                # Rende il campo appropriato
                if field_type == 'text':
                    form_data[field_name] = st.text_input(
                        field_label,
                        value=field_value,
                        help=f"{'Obbligatorio' if field_required else 'Opzionale'}"
                    )
                elif field_type == 'email':
                    form_data[field_name] = st.text_input(
                        field_label,
                        value=field_value,
                        type='email',
                        help=f"{'Obbligatorio' if field_required else 'Opzionale'}"
                    )
                elif field_type == 'password':
                    form_data[field_name] = st.text_input(
                        field_label,
                        value=field_value,
                        type='password',
                        help=f"{'Obbligatorio' if field_required else 'Opzionale'}"
                    )
                elif field_type == 'number':
                    form_data[field_name] = st.number_input(
                        field_label,
                        value=float(field_value) if field_value else 0.0,
                        step=field.get('step', 1.0),
                        help=f"{'Obbligatorio' if field_required else 'Opzionale'}"
                    )
                elif field_type == 'date':
                    form_data[field_name] = st.date_input(
                        field_label,
                        value=datetime.strptime(field_value, '%Y-%m-%d').date() if field_value else date.today(),
                        help=f"{'Obbligatorio' if field_required else 'Opzionale'}"
                    )
                elif field_type == 'select':
                    form_data[field_name] = st.selectbox(
                        field_label,
                        options=field.get('options', []),
                        index=field.get('options', []).index(field_value) if field_value in field.get('options', []) else 0,
                        help=f"{'Obbligatorio' if field_required else 'Opzionale'}"
                    )
                elif field_type == 'textarea':
                    form_data[field_name] = st.text_area(
                        field_label,
                        value=field_value,
                        help=f"{'Obbligatorio' if field_required else 'Opzionale'}"
                    )
                elif field_type == 'url':
                    form_data[field_name] = st.text_input(
                        field_label,
                        value=field_value,
                        help=f"{'Obbligatorio' if field_required else 'Opzionale'}"
                    )
            
            # Pulsanti submit
            col1, col2 = st.columns(2)
            
            with col1:
                submit_button = st.form_submit_button(
                    "💾 Salva",
                    use_container_width=True,
                    type="primary"
                )
            
            with col2:
                cancel_button = st.form_submit_button(
                    "❌ Annulla",
                    use_container_width=True
                )
            
            if submit_button:
                # Valida i campi obbligatori
                missing_fields = []
                for field in config['fields']:
                    if field.get('required', False) and not form_data.get(field['name']):
                        missing_fields.append(field['label'])
                
                if missing_fields:
                    st.error(f"❌ Campi obbligatori mancanti: {', '.join(missing_fields)}")
                    return None
                
                return form_data
            
            if cancel_button:
                return None
        
        return None

class UnifiedTable:
    """Tabella unificata per tutti i progetti"""
    
    def __init__(self, table_type: str, project_type: str = None):
        """
        Inizializza tabella unificata
        
        Args:
            table_type: Tipo di tabella ('lead', 'client', 'broker', etc.)
            project_type: Tipo di progetto ('lead', 'cpa', 'prop')
        """
        self.table_type = table_type
        self.project_type = project_type or get_current_project()
        self.db_manager = get_database_manager(self.project_type)
        self.app_config = get_app_config()
        
        # Configurazioni tabella per tipo
        self.table_configs = self._init_table_configs()
    
    def _init_table_configs(self) -> Dict[str, Dict[str, Any]]:
        """Inizializza configurazioni tabella per tipo"""
        return {
            'lead': {
                'title': '🎯 Gestione Lead',
                'table': 'leads',
                'columns': ['id', 'name', 'email', 'phone', 'company', 'budget', 'expected_close_date', 'created_at'],
                'display_columns': ['ID', 'Nome', 'Email', 'Telefono', 'Azienda', 'Budget', 'Data Chiusura', 'Creato'],
                'search_columns': ['name', 'email', 'company'],
                'sort_column': 'created_at'
            },
            'client': {
                'title': '💼 Gestione Clienti CPA',
                'table': 'clienti',
                'columns': ['id', 'nome_cliente', 'email', 'broker', 'deposito', 'piattaforma', 'data_registrazione', 'created_at'],
                'display_columns': ['ID', 'Nome', 'Email', 'Broker', 'Deposito', 'Piattaforma', 'Data Registrazione', 'Creato'],
                'search_columns': ['nome_cliente', 'email', 'broker'],
                'sort_column': 'created_at'
            },
            'broker': {
                'title': '🧮 Gestione Broker',
                'table': 'brokers',
                'columns': ['id', 'nome_broker', 'tipo_broker', 'regolamentazione', 'paese', 'spread_minimo', 'commissioni', 'created_at'],
                'display_columns': ['ID', 'Nome', 'Tipo', 'Regolamentazione', 'Paese', 'Spread', 'Commissioni', 'Creato'],
                'search_columns': ['nome_broker', 'regolamentazione', 'paese'],
                'sort_column': 'created_at'
            }
        }
    
    def render_table(self, data: List[Dict[str, Any]] = None, show_actions: bool = True) -> Optional[Dict[str, Any]]:
        """Rende la tabella"""
        config = self.table_configs.get(self.table_type, {})
        if not config:
            st.error(f"❌ Tipo tabella non supportato: {self.table_type}")
            return None
        
        st.markdown(f"### {config['title']}")
        
        # Carica dati se non forniti
        if data is None:
            data = self.db_manager.get_all_records(config['table'])
        
        if not data:
            st.info("📭 Nessun dato disponibile")
            return None
        
        # Filtri di ricerca
        search_term = st.text_input(
            "🔍 Cerca",
            placeholder="Inserisci termine di ricerca...",
            help=f"Cerca in: {', '.join(config['search_columns'])}"
        )
        
        # Filtra dati
        if search_term:
            filtered_data = []
            for record in data:
                for search_col in config['search_columns']:
                    if search_term.lower() in str(record.get(search_col, '')).lower():
                        filtered_data.append(record)
                        break
            data = filtered_data
        
        # Converte in DataFrame
        df = pd.DataFrame(data)
        
        if df.empty:
            st.info("📭 Nessun risultato trovato")
            return None
        
        # Seleziona colonne da mostrare
        display_columns = config['display_columns']
        table_columns = config['columns']
        
        # Crea DataFrame per visualizzazione
        display_df = df[table_columns].copy()
        display_df.columns = display_columns
        
        # Aggiungi colonna azioni se richiesta
        if show_actions:
            display_df['Azioni'] = 'Modifica | Elimina'
        
        # Mostra tabella
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
        
        # Statistiche
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Totale Record", len(data))
        
        with col2:
            st.metric("🔍 Risultati Filtrati", len(data))
        
        with col3:
            if data:
                last_created = max([record.get('created_at', '') for record in data])
                st.metric("📅 Ultimo Creato", last_created[:10] if last_created else 'N/A')
        
        return data

class UnifiedChart:
    """Grafico unificato per tutti i progetti"""
    
    def __init__(self, chart_type: str, project_type: str = None):
        """
        Inizializza grafico unificato
        
        Args:
            chart_type: Tipo di grafico ('bar', 'line', 'pie', 'scatter')
            project_type: Tipo di progetto ('lead', 'cpa', 'prop')
        """
        self.chart_type = chart_type
        self.project_type = project_type or get_current_project()
        self.app_config = get_app_config()
    
    def render_chart(self, data: List[Dict[str, Any]], x_column: str, y_column: str = None, 
                    title: str = None, color_column: str = None) -> None:
        """Rende il grafico"""
        if not data:
            st.info("📭 Nessun dato disponibile per il grafico")
            return
        
        df = pd.DataFrame(data)
        
        if df.empty:
            st.info("📭 Nessun dato disponibile per il grafico")
            return
        
        # Crea grafico basato sul tipo
        if self.chart_type == 'bar':
            fig = px.bar(
                df,
                x=x_column,
                y=y_column,
                title=title or f"Grafico a Barre - {x_column}",
                color=color_column,
                template=self.app_config['ui']['chart_template']
            )
        elif self.chart_type == 'line':
            fig = px.line(
                df,
                x=x_column,
                y=y_column,
                title=title or f"Grafico a Linee - {x_column}",
                color=color_column,
                template=self.app_config['ui']['chart_template']
            )
        elif self.chart_type == 'pie':
            fig = px.pie(
                df,
                names=x_column,
                values=y_column,
                title=title or f"Grafico a Torta - {x_column}",
                template=self.app_config['ui']['chart_template']
            )
        elif self.chart_type == 'scatter':
            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                title=title or f"Grafico a Dispersione - {x_column}",
                color=color_column,
                template=self.app_config['ui']['chart_template']
            )
        else:
            st.error(f"❌ Tipo grafico non supportato: {self.chart_type}")
            return
        
        # Mostra grafico
        st.plotly_chart(
            fig,
            use_container_width=True,
            height=self.app_config['ui']['chart_height']
        )

class UnifiedMetrics:
    """Metriche unificate per tutti i progetti"""
    
    def __init__(self, project_type: str = None):
        """
        Inizializza metriche unificate
        
        Args:
            project_type: Tipo di progetto ('lead', 'cpa', 'prop')
        """
        self.project_type = project_type or get_current_project()
        self.db_manager = get_database_manager(self.project_type)
    
    def render_metrics(self, metrics_data: Dict[str, Any] = None) -> None:
        """Rende le metriche"""
        if metrics_data is None:
            metrics_data = self._get_default_metrics()
        
        # Layout metriche
        cols = st.columns(len(metrics_data))
        
        for i, (metric_name, metric_value) in enumerate(metrics_data.items()):
            with cols[i]:
                st.metric(
                    metric_name,
                    metric_value['value'],
                    delta=metric_value.get('delta'),
                    help=metric_value.get('help')
                )
    
    def _get_default_metrics(self) -> Dict[str, Any]:
        """Ottiene metriche di default per progetto"""
        if self.project_type == 'lead':
            return {
                "🎯 Lead Totali": {"value": "0", "help": "Numero totale di lead"},
                "📞 Lead Contattati": {"value": "0", "help": "Lead già contattati"},
                "💰 Budget Totale": {"value": "€0", "help": "Budget totale dei lead"},
                "📅 Lead Oggi": {"value": "0", "help": "Lead creati oggi"}
            }
        elif self.project_type == 'cpa':
            return {
                "💼 Clienti Totali": {"value": "0", "help": "Numero totale di clienti"},
                "🏦 Broker Attivi": {"value": "0", "help": "Broker con clienti attivi"},
                "💰 Depositi Totali": {"value": "€0", "help": "Depositi totali"},
                "📅 Clienti Oggi": {"value": "0", "help": "Clienti registrati oggi"}
            }
        elif self.project_type == 'prop':
            return {
                "🧮 Broker Totali": {"value": "0", "help": "Numero totale di broker"},
                "🏛️ Prop Firm Attive": {"value": "0", "help": "Prop firm attive"},
                "💰 Wallet Totali": {"value": "0", "help": "Numero totale di wallet"},
                "📅 Broker Oggi": {"value": "0", "help": "Broker aggiunti oggi"}
            }
        else:
            return {}

# Funzioni di utilità
def get_form(form_type: str, project_type: str = None) -> UnifiedForm:
    """Ottiene un form unificato"""
    return UnifiedForm(form_type, project_type)

def get_table(table_type: str, project_type: str = None) -> UnifiedTable:
    """Ottiene una tabella unificata"""
    return UnifiedTable(table_type, project_type)

def get_chart(chart_type: str, project_type: str = None) -> UnifiedChart:
    """Ottiene un grafico unificato"""
    return UnifiedChart(chart_type, project_type)

def get_metrics(project_type: str = None) -> UnifiedMetrics:
    """Ottiene metriche unificate"""
    return UnifiedMetrics(project_type)
