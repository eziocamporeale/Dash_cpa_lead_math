#!/usr/bin/env python3
"""
🛠️ COMMON UTILS - Dashboard Unificata
Utility comuni per tutti i progetti
Creato da Ezio Camporeale
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import json
import hashlib
import secrets
from typing import Dict, List, Optional, Any, Union
import plotly.express as px
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

class CommonUtils:
    """
    🛠️ Utility comuni per tutti i progetti
    
    Funzionalità:
    - Formattazione dati
    - Validazione input
    - Calcoli matematici
    - Gestione date
    - Esportazione dati
    """
    
    @staticmethod
    def format_currency(amount: float, currency: str = "EUR") -> str:
        """Formatta valuta"""
        if currency == "EUR":
            return f"€{amount:,.2f}"
        elif currency == "USD":
            return f"${amount:,.2f}"
        else:
            return f"{amount:,.2f} {currency}"
    
    @staticmethod
    def format_percentage(value: float, decimals: int = 2) -> str:
        """Formatta percentuale"""
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def format_number(value: float, decimals: int = 0) -> str:
        """Formatta numero"""
        return f"{value:,.{decimals}f}"
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Valida telefono"""
        import re
        pattern = r'^\+?[\d\s\-\(\)]{10,}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def calculate_roi(initial: float, final: float) -> float:
        """Calcola ROI"""
        if initial == 0:
            return 0
        return ((final - initial) / initial) * 100
    
    @staticmethod
    def calculate_growth_rate(old_value: float, new_value: float) -> float:
        """Calcola tasso di crescita"""
        if old_value == 0:
            return 0
        return ((new_value - old_value) / old_value) * 100
    
    @staticmethod
    def generate_unique_id(prefix: str = "") -> str:
        """Genera ID univoco"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = secrets.token_hex(4)
        return f"{prefix}{timestamp}_{random_part}"
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        """Verifica password"""
        try:
            salt, password_hash = stored_hash.split(':')
            new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return new_hash.hex() == password_hash
        except:
            return False
    
    @staticmethod
    def export_to_csv(data: pd.DataFrame, filename: str = None) -> str:
        """Esporta dati in CSV"""
        if filename is None:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        csv_data = data.to_csv(index=False)
        return csv_data
    
    @staticmethod
    def export_to_excel(data: pd.DataFrame, filename: str = None) -> bytes:
        """Esporta dati in Excel"""
        if filename is None:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            data.to_excel(writer, sheet_name='Data', index=False)
        return output.getvalue()
    
    @staticmethod
    def create_date_range(start_date: datetime, end_date: datetime) -> List[datetime]:
        """Crea range di date"""
        delta = end_date - start_date
        return [start_date + timedelta(days=i) for i in range(delta.days + 1)]
    
    @staticmethod
    def get_month_name(month_number: int) -> str:
        """Ottiene nome mese"""
        months = [
            "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
        ]
        return months[month_number - 1] if 1 <= month_number <= 12 else "Sconosciuto"
    
    @staticmethod
    def create_progress_bar(current: float, total: float, label: str = "") -> None:
        """Crea barra di progresso"""
        if total == 0:
            progress = 0
        else:
            progress = current / total
        
        st.progress(progress)
        if label:
            st.caption(f"{label}: {current}/{total} ({progress:.1%})")
    
    @staticmethod
    def show_metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal") -> None:
        """Mostra card metrica"""
        st.metric(
            label=title,
            value=value,
            delta=delta,
            delta_color=delta_color
        )
    
    @staticmethod
    def create_line_chart(data: pd.DataFrame, x: str, y: str, title: str = "") -> go.Figure:
        """Crea grafico a linee"""
        fig = px.line(data, x=x, y=y, title=title)
        return fig
    
    @staticmethod
    def create_bar_chart(data: pd.DataFrame, x: str, y: str, title: str = "") -> go.Figure:
        """Crea grafico a barre"""
        fig = px.bar(data, x=x, y=y, title=title)
        return fig
    
    @staticmethod
    def create_pie_chart(data: pd.DataFrame, names: str, values: str, title: str = "") -> go.Figure:
        """Crea grafico a torta"""
        fig = px.pie(data, names=names, values=values, title=title)
        return fig
    
    @staticmethod
    def create_scatter_chart(data: pd.DataFrame, x: str, y: str, title: str = "") -> go.Figure:
        """Crea grafico a dispersione"""
        fig = px.scatter(data, x=x, y=y, title=title)
        return fig
    
    @staticmethod
    def filter_dataframe(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Filtra DataFrame"""
        filtered_df = df.copy()
        
        for column, value in filters.items():
            if column in filtered_df.columns and value is not None:
                if isinstance(value, str):
                    filtered_df = filtered_df[filtered_df[column].str.contains(value, case=False, na=False)]
                elif isinstance(value, list):
                    filtered_df = filtered_df[filtered_df[column].isin(value)]
                else:
                    filtered_df = filtered_df[filtered_df[column] == value]
        
        return filtered_df
    
    @staticmethod
    def calculate_statistics(data: pd.Series) -> Dict[str, float]:
        """Calcola statistiche"""
        return {
            'mean': data.mean(),
            'median': data.median(),
            'std': data.std(),
            'min': data.min(),
            'max': data.max(),
            'count': data.count()
        }
    
    @staticmethod
    def create_summary_table(data: pd.DataFrame, group_by: str, agg_columns: List[str]) -> pd.DataFrame:
        """Crea tabella riassuntiva"""
        agg_dict = {}
        for col in agg_columns:
            if col in data.columns:
                agg_dict[col] = ['sum', 'mean', 'count']
        
        summary = data.groupby(group_by).agg(agg_dict).round(2)
        summary.columns = ['_'.join(col).strip() for col in summary.columns]
        
        return summary.reset_index()
    
    @staticmethod
    def log_activity(activity: str, user: str = "System", project: str = "general") -> None:
        """Log attività"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {project.upper()} - {user}: {activity}"
        logger.info(log_message)
    
    @staticmethod
    def show_error_message(error: str, details: str = "") -> None:
        """Mostra messaggio di errore"""
        st.error(f"❌ {error}")
        if details:
            st.caption(f"🔍 Dettagli: {details}")
    
    @staticmethod
    def show_success_message(message: str) -> None:
        """Mostra messaggio di successo"""
        st.success(f"✅ {message}")
    
    @staticmethod
    def show_warning_message(message: str) -> None:
        """Mostra messaggio di avviso"""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def show_info_message(message: str) -> None:
        """Mostra messaggio informativo"""
        st.info(f"ℹ️ {message}")
    
    @staticmethod
    def create_download_button(data: Union[pd.DataFrame, str], filename: str, file_type: str = "csv") -> None:
        """Crea pulsante download"""
        if file_type == "csv":
            if isinstance(data, pd.DataFrame):
                csv_data = data.to_csv(index=False)
            else:
                csv_data = data
            st.download_button(
                label="📥 Scarica CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv"
            )
        elif file_type == "excel":
            if isinstance(data, pd.DataFrame):
                excel_data = CommonUtils.export_to_excel(data)
            else:
                excel_data = data
            st.download_button(
                label="📥 Scarica Excel",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    @staticmethod
    def create_confirmation_dialog(message: str, action: str) -> bool:
        """Crea dialog di conferma"""
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Conferma", use_container_width=True):
                return True
        
        with col2:
            if st.button("❌ Annulla", use_container_width=True):
                return False
        
        return False
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Formatta durata"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}m {seconds % 60}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """Ottiene dimensione file in MB"""
        import os
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        return 0.0
    
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Pulisce DataFrame"""
        # Rimuovi colonne completamente vuote
        df = df.dropna(axis=1, how='all')
        
        # Rimuovi righe completamente vuote
        df = df.dropna(axis=0, how='all')
        
        # Rimuovi spazi extra
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
        
        return df
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> Dict[str, Any]:
        """Valida DataFrame"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Controlla colonne richieste
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Colonne mancanti: {missing_columns}")
        
        # Controlla righe vuote
        empty_rows = df.isnull().all(axis=1).sum()
        if empty_rows > 0:
            validation_result['warnings'].append(f"{empty_rows} righe completamente vuote")
        
        # Controlla duplicati
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            validation_result['warnings'].append(f"{duplicates} righe duplicate")
        
        return validation_result
