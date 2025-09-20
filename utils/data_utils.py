#!/usr/bin/env python3
"""
📊 DATA UTILS - Dashboard Unificata
Utility per gestione dati
Creato da Ezio Camporeale
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any, Tuple
import json

logger = logging.getLogger(__name__)

class DataUtils:
    """
    📊 Utility per gestione dati
    
    Funzionalità:
    - Trasformazione dati
    - Aggregazioni
    - Filtri avanzati
    - Calcoli statistici
    """
    
    @staticmethod
    def aggregate_by_period(data: pd.DataFrame, date_column: str, value_column: str, period: str = 'M') -> pd.DataFrame:
        """Aggrega dati per periodo"""
        data[date_column] = pd.to_datetime(data[date_column])
        data.set_index(date_column, inplace=True)
        
        aggregated = data[value_column].resample(period).agg(['sum', 'mean', 'count'])
        aggregated.columns = [f'{value_column}_{col}' for col in aggregated.columns]
        
        return aggregated.reset_index()
    
    @staticmethod
    def calculate_moving_average(data: pd.Series, window: int = 7) -> pd.Series:
        """Calcola media mobile"""
        return data.rolling(window=window).mean()
    
    @staticmethod
    def calculate_growth_rate(data: pd.Series) -> pd.Series:
        """Calcola tasso di crescita"""
        return data.pct_change() * 100
    
    @staticmethod
    def detect_outliers(data: pd.Series, method: str = 'iqr') -> pd.Series:
        """Rileva outlier"""
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (data < lower_bound) | (data > upper_bound)
        elif method == 'zscore':
            z_scores = np.abs((data - data.mean()) / data.std())
            return z_scores > 3
        else:
            return pd.Series([False] * len(data))
    
    @staticmethod
    def fill_missing_values(data: pd.DataFrame, method: str = 'forward') -> pd.DataFrame:
        """Riempie valori mancanti"""
        if method == 'forward':
            return data.fillna(method='ffill')
        elif method == 'backward':
            return data.fillna(method='bfill')
        elif method == 'mean':
            return data.fillna(data.mean())
        elif method == 'median':
            return data.fillna(data.median())
        else:
            return data.fillna(0)
    
    @staticmethod
    def normalize_data(data: pd.Series, method: str = 'minmax') -> pd.Series:
        """Normalizza dati"""
        if method == 'minmax':
            return (data - data.min()) / (data.max() - data.min())
        elif method == 'zscore':
            return (data - data.mean()) / data.std()
        else:
            return data
    
    @staticmethod
    def create_categories(data: pd.Series, bins: int = 5, labels: List[str] = None) -> pd.Series:
        """Crea categorie"""
        if labels is None:
            labels = [f'Categoria {i+1}' for i in range(bins)]
        
        return pd.cut(data, bins=bins, labels=labels, include_lowest=True)
    
    @staticmethod
    def calculate_correlation_matrix(data: pd.DataFrame) -> pd.DataFrame:
        """Calcola matrice di correlazione"""
        numeric_data = data.select_dtypes(include=[np.number])
        return numeric_data.corr()
    
    @staticmethod
    def pivot_table(data: pd.DataFrame, index: str, columns: str, values: str, aggfunc: str = 'sum') -> pd.DataFrame:
        """Crea tabella pivot"""
        return data.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc, fill_value=0)
    
    @staticmethod
    def group_by_multiple(data: pd.DataFrame, group_columns: List[str], agg_dict: Dict[str, List[str]]) -> pd.DataFrame:
        """Raggruppa per più colonne"""
        grouped = data.groupby(group_columns).agg(agg_dict)
        grouped.columns = ['_'.join(col).strip() for col in grouped.columns]
        return grouped.reset_index()
    
    @staticmethod
    def calculate_percentiles(data: pd.Series, percentiles: List[float] = [25, 50, 75, 90, 95, 99]) -> Dict[float, float]:
        """Calcola percentili"""
        return {p: data.quantile(p/100) for p in percentiles}
    
    @staticmethod
    def create_time_series_features(data: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """Crea feature temporali"""
        data[date_column] = pd.to_datetime(data[date_column])
        
        data['year'] = data[date_column].dt.year
        data['month'] = data[date_column].dt.month
        data['day'] = data[date_column].dt.day
        data['weekday'] = data[date_column].dt.weekday
        data['quarter'] = data[date_column].dt.quarter
        data['is_weekend'] = data[date_column].dt.weekday >= 5
        
        return data
    
    @staticmethod
    def calculate_metrics(data: pd.DataFrame, value_column: str, group_column: str = None) -> Dict[str, Any]:
        """Calcola metriche"""
        if group_column:
            grouped_data = data.groupby(group_column)[value_column]
        else:
            grouped_data = data[value_column]
        
        metrics = {
            'count': grouped_data.count(),
            'sum': grouped_data.sum(),
            'mean': grouped_data.mean(),
            'median': grouped_data.median(),
            'std': grouped_data.std(),
            'min': grouped_data.min(),
            'max': grouped_data.max(),
            'q25': grouped_data.quantile(0.25),
            'q75': grouped_data.quantile(0.75)
        }
        
        return metrics
    
    @staticmethod
    def create_summary_statistics(data: pd.DataFrame) -> pd.DataFrame:
        """Crea statistiche riassuntive"""
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        summary = pd.DataFrame({
            'count': data[numeric_columns].count(),
            'mean': data[numeric_columns].mean(),
            'std': data[numeric_columns].std(),
            'min': data[numeric_columns].min(),
            '25%': data[numeric_columns].quantile(0.25),
            '50%': data[numeric_columns].quantile(0.50),
            '75%': data[numeric_columns].quantile(0.75),
            'max': data[numeric_columns].max()
        })
        
        return summary.T
    
    @staticmethod
    def filter_by_date_range(data: pd.DataFrame, date_column: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Filtra per range di date"""
        data[date_column] = pd.to_datetime(data[date_column])
        return data[(data[date_column] >= start_date) & (data[date_column] <= end_date)]
    
    @staticmethod
    def create_rolling_statistics(data: pd.Series, window: int = 7, functions: List[str] = ['mean', 'std']) -> pd.DataFrame:
        """Crea statistiche rolling"""
        rolling_stats = pd.DataFrame()
        
        for func in functions:
            if func == 'mean':
                rolling_stats[f'rolling_mean_{window}'] = data.rolling(window=window).mean()
            elif func == 'std':
                rolling_stats[f'rolling_std_{window}'] = data.rolling(window=window).std()
            elif func == 'min':
                rolling_stats[f'rolling_min_{window}'] = data.rolling(window=window).min()
            elif func == 'max':
                rolling_stats[f'rolling_max_{window}'] = data.rolling(window=window).max()
        
        return rolling_stats
    
    @staticmethod
    def calculate_trend(data: pd.Series) -> Dict[str, float]:
        """Calcola trend"""
        x = np.arange(len(data))
        y = data.values
        
        # Rimuovi NaN
        mask = ~np.isnan(y)
        x_clean = x[mask]
        y_clean = y[mask]
        
        if len(x_clean) < 2:
            return {'slope': 0, 'r_squared': 0, 'trend': 'flat'}
        
        # Regressione lineare
        slope, intercept = np.polyfit(x_clean, y_clean, 1)
        
        # R-squared
        y_pred = slope * x_clean + intercept
        ss_res = np.sum((y_clean - y_pred) ** 2)
        ss_tot = np.sum((y_clean - np.mean(y_clean)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Determina trend
        if slope > 0.01:
            trend = 'upward'
        elif slope < -0.01:
            trend = 'downward'
        else:
            trend = 'flat'
        
        return {
            'slope': slope,
            'r_squared': r_squared,
            'trend': trend
        }
    
    @staticmethod
    def create_cohort_analysis(data: pd.DataFrame, user_column: str, date_column: str, value_column: str) -> pd.DataFrame:
        """Crea analisi cohort"""
        data[date_column] = pd.to_datetime(data[date_column])
        
        # Prima data per ogni utente
        first_purchase = data.groupby(user_column)[date_column].min().reset_index()
        first_purchase.columns = [user_column, 'first_date']
        
        # Merge con dati originali
        cohort_data = data.merge(first_purchase, on=user_column)
        
        # Calcola periodo
        cohort_data['period'] = (cohort_data[date_column] - cohort_data['first_date']).dt.days
        
        # Pivot table
        cohort_table = cohort_data.pivot_table(
            index='first_date',
            columns='period',
            values=value_column,
            aggfunc='sum',
            fill_value=0
        )
        
        return cohort_table
    
    @staticmethod
    def calculate_conversion_funnel(data: pd.DataFrame, stage_column: str, user_column: str) -> pd.DataFrame:
        """Calcola funnel di conversione"""
        # Conta utenti per stage
        stage_counts = data.groupby(stage_column)[user_column].nunique().reset_index()
        stage_counts.columns = ['stage', 'users']
        
        # Calcola conversioni
        stage_counts['conversion_rate'] = stage_counts['users'] / stage_counts['users'].iloc[0] * 100
        
        return stage_counts
    
    @staticmethod
    def detect_seasonality(data: pd.Series, period: int = 12) -> Dict[str, Any]:
        """Rileva stagionalità"""
        if len(data) < period * 2:
            return {'has_seasonality': False, 'strength': 0}
        
        # Decomposizione stagionale
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        try:
            decomposition = seasonal_decompose(data.dropna(), model='additive', period=period)
            seasonal_strength = np.var(decomposition.seasonal) / np.var(data.dropna())
            
            return {
                'has_seasonality': seasonal_strength > 0.1,
                'strength': seasonal_strength,
                'seasonal_component': decomposition.seasonal
            }
        except:
            return {'has_seasonality': False, 'strength': 0}
    
    @staticmethod
    def create_benchmark_comparison(data: pd.DataFrame, benchmark_column: str, value_column: str) -> pd.DataFrame:
        """Crea confronto con benchmark"""
        benchmark_value = data[benchmark_column].mean()
        
        comparison = data.copy()
        comparison['vs_benchmark'] = comparison[value_column] - benchmark_value
        comparison['vs_benchmark_pct'] = (comparison[value_column] / benchmark_value - 1) * 100
        
        return comparison
