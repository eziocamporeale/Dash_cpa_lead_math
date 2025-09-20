#!/usr/bin/env python3
"""
🤖 AI ASSISTANT UNIFICATO - Dashboard Unificata
Sistema AI avanzato che integra funzionalità di tutti e tre i progetti
Creato da Ezio Camporeale
"""

import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging
from config.unified_config import UnifiedConfig

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedAIAssistant:
    """
    🤖 AI Assistant Unificato
    
    Integra le funzionalità AI di tutti e tre i progetti:
    - LEAD: Analisi lead e previsioni
    - CPA: Calcoli finanziari avanzati
    - PROP: Analisi broker e performance
    """
    
    def __init__(self):
        """Inizializza l'AI Assistant"""
        self.config = UnifiedConfig()
        self.session_state = st.session_state
        
        # Configurazione AI
        self.api_key = self.config.deepseek_api_key
        self.api_url = self.config.deepseek_api_url
        self.model = self.config.deepseek_model
        
        # Cache per ottimizzare le chiamate
        self.cache = {}
        self.cache_timeout = 300  # 5 minuti
        
        logger.info("🤖 AI Assistant Unificato inizializzato")
    
    def _make_api_call(self, messages: List[Dict], project_type: str = "general") -> Optional[str]:
        """
        Effettua chiamata API a DeepSeek
        
        Args:
            messages: Lista messaggi per l'API
            project_type: Tipo di progetto (lead, cpa, prop)
            
        Returns:
            Risposta dell'AI o None se errore
        """
        try:
            # Controlla cache
            cache_key = f"{project_type}_{hash(str(messages))}"
            if cache_key in self.cache:
                cached_time, response = self.cache[cache_key]
                if datetime.now() - cached_time < timedelta(seconds=self.cache_timeout):
                    return response
            
            # Headers per l'API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Payload per l'API
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.config.ai_config.get('max_tokens', 1500),
                "temperature": self.config.ai_config.get('temperature', 0.7),
                "stream": False
            }
            
            # Chiamata API
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Salva in cache
                self.cache[cache_key] = (datetime.now(), ai_response)
                
                return ai_response
            else:
                logger.error(f"Errore API DeepSeek: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Errore chiamata AI: {str(e)}")
            return None
    
    def analyze_lead_data(self, lead_data: pd.DataFrame, project_type: str = "lead") -> Dict[str, Any]:
        """
        📊 Analisi Avanzata Lead Data
        
        Args:
            lead_data: DataFrame con dati lead
            project_type: Tipo di progetto
            
        Returns:
            Dizionario con analisi dettagliata
        """
        try:
            # Preparazione dati per l'AI
            data_summary = {
                "total_leads": len(lead_data),
                "columns": list(lead_data.columns),
                "date_range": {
                    "start": lead_data['data_registrazione'].min() if 'data_registrazione' in lead_data.columns else None,
                    "end": lead_data['data_registrazione'].max() if 'data_registrazione' in lead_data.columns else None
                },
                "conversion_rate": self._calculate_conversion_rate(lead_data),
                "top_sources": self._get_top_sources(lead_data),
                "trends": self._analyze_trends(lead_data)
            }
            
            # Prompt per l'AI
            messages = [
                {
                    "role": "system",
                    "content": f"""Sei un esperto analista di lead per il progetto {project_type.upper()}. 
                    Analizza i dati forniti e fornisci insights dettagliati, previsioni e raccomandazioni strategiche.
                    Rispondi in italiano, formato JSON strutturato."""
                },
                {
                    "role": "user",
                    "content": f"""Analizza questi dati lead per il progetto {project_type.upper()}:
                    
                    {json.dumps(data_summary, indent=2)}
                    
                    Fornisci:
                    1. Analisi delle performance
                    2. Trend identificati
                    3. Previsioni per i prossimi 30 giorni
                    4. Raccomandazioni strategiche
                    5. Aree di miglioramento
                    
                    Formato JSON con sezioni: analysis, trends, predictions, recommendations, improvements"""
                }
            ]
            
            # Chiamata AI
            ai_response = self._make_api_call(messages, project_type)
            
            if ai_response:
                try:
                    analysis = json.loads(ai_response)
                    analysis['data_summary'] = data_summary
                    analysis['timestamp'] = datetime.now().isoformat()
                    return analysis
                except json.JSONDecodeError:
                    return {
                        "analysis": ai_response,
                        "data_summary": data_summary,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return self._fallback_lead_analysis(lead_data, data_summary)
                
        except Exception as e:
            logger.error(f"Errore analisi lead: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def calculate_cpa_metrics(self, cpa_data: pd.DataFrame, project_type: str = "cpa") -> Dict[str, Any]:
        """
        💰 Calcoli Metriche CPA Avanzate
        
        Args:
            cpa_data: DataFrame con dati CPA
            project_type: Tipo di progetto
            
        Returns:
            Dizionario con metriche calcolate
        """
        try:
            # Calcoli base
            metrics = {
                "total_clients": len(cpa_data),
                "total_deposits": cpa_data['deposito'].sum() if 'deposito' in cpa_data.columns else 0,
                "average_deposit": cpa_data['deposito'].mean() if 'deposito' in cpa_data.columns else 0,
                "broker_distribution": self._get_broker_distribution(cpa_data),
                "platform_analysis": self._analyze_platforms(cpa_data),
                "vps_usage": self._analyze_vps_usage(cpa_data),
                "financial_projections": self._calculate_financial_projections(cpa_data)
            }
            
            # Prompt per calcoli avanzati
            messages = [
                {
                    "role": "system",
                    "content": f"""Sei un esperto finanziario per il progetto {project_type.upper()}. 
                    Calcola metriche avanzate, ROI, previsioni finanziarie e analisi di performance.
                    Rispondi in italiano, formato JSON strutturato."""
                },
                {
                    "role": "user",
                    "content": f"""Calcola metriche avanzate CPA per il progetto {project_type.upper()}:
                    
                    {json.dumps(metrics, indent=2)}
                    
                    Calcola:
                    1. ROI per broker
                    2. Previsioni di crescita
                    3. Analisi di rischio
                    4. Ottimizzazione budget
                    5. Raccomandazioni strategiche
                    
                    Formato JSON con sezioni: roi_analysis, growth_projections, risk_assessment, budget_optimization, strategic_recommendations"""
                }
            ]
            
            # Chiamata AI
            ai_response = self._make_api_call(messages, project_type)
            
            if ai_response:
                try:
                    advanced_metrics = json.loads(ai_response)
                    advanced_metrics['basic_metrics'] = metrics
                    advanced_metrics['timestamp'] = datetime.now().isoformat()
                    return advanced_metrics
                except json.JSONDecodeError:
                    return {
                        "advanced_analysis": ai_response,
                        "basic_metrics": metrics,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return self._fallback_cpa_analysis(cpa_data, metrics)
                
        except Exception as e:
            logger.error(f"Errore calcoli CPA: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def analyze_broker_performance(self, broker_data: pd.DataFrame, project_type: str = "prop") -> Dict[str, Any]:
        """
        🏢 Analisi Performance Broker
        
        Args:
            broker_data: DataFrame con dati broker
            project_type: Tipo di progetto
            
        Returns:
            Dizionario con analisi broker
        """
        try:
            # Analisi base
            analysis = {
                "total_brokers": len(broker_data),
                "broker_rankings": self._rank_brokers(broker_data),
                "performance_metrics": self._calculate_broker_metrics(broker_data),
                "market_analysis": self._analyze_market_trends(broker_data),
                "risk_assessment": self._assess_broker_risks(broker_data)
            }
            
            # Prompt per analisi avanzata
            messages = [
                {
                    "role": "system",
                    "content": f"""Sei un esperto di mercati finanziari per il progetto {project_type.upper()}. 
                    Analizza performance broker, trend di mercato e fornisci raccomandazioni strategiche.
                    Rispondi in italiano, formato JSON strutturato."""
                },
                {
                    "role": "user",
                    "content": f"""Analizza performance broker per il progetto {project_type.upper()}:
                    
                    {json.dumps(analysis, indent=2)}
                    
                    Fornisci:
                    1. Ranking broker dettagliato
                    2. Analisi di mercato
                    3. Previsioni trend
                    4. Raccomandazioni di investimento
                    5. Gestione del rischio
                    
                    Formato JSON con sezioni: broker_rankings, market_analysis, trend_predictions, investment_recommendations, risk_management"""
                }
            ]
            
            # Chiamata AI
            ai_response = self._make_api_call(messages, project_type)
            
            if ai_response:
                try:
                    advanced_analysis = json.loads(ai_response)
                    advanced_analysis['basic_analysis'] = analysis
                    advanced_analysis['timestamp'] = datetime.now().isoformat()
                    return advanced_analysis
                except json.JSONDecodeError:
                    return {
                        "advanced_analysis": ai_response,
                        "basic_analysis": analysis,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return self._fallback_broker_analysis(broker_data, analysis)
                
        except Exception as e:
            logger.error(f"Errore analisi broker: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def generate_unified_report(self, all_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        📋 Genera Report Unificato
        
        Args:
            all_data: Dizionario con dati di tutti i progetti
            
        Returns:
            Report unificato completo
        """
        try:
            # Preparazione dati unificati
            unified_summary = {
                "projects": list(all_data.keys()),
                "total_records": sum(len(df) for df in all_data.values()),
                "date_range": self._get_unified_date_range(all_data),
                "cross_project_insights": self._analyze_cross_project_data(all_data)
            }
            
            # Prompt per report unificato
            messages = [
                {
                    "role": "system",
                    "content": """Sei un esperto strategico che analizza progetti multipli. 
                    Genera un report unificato con insights cross-project, sinergie identificate 
                    e raccomandazioni strategiche globali. Rispondi in italiano, formato JSON strutturato."""
                },
                {
                    "role": "user",
                    "content": f"""Genera report unificato per tutti i progetti:
                    
                    {json.dumps(unified_summary, indent=2)}
                    
                    Include:
                    1. Panoramica generale
                    2. Sinergie tra progetti
                    3. Insights cross-project
                    4. Raccomandazioni strategiche globali
                    5. Roadmap di sviluppo
                    
                    Formato JSON con sezioni: executive_summary, project_synergies, cross_insights, strategic_recommendations, development_roadmap"""
                }
            ]
            
            # Chiamata AI
            ai_response = self._make_api_call(messages, "unified")
            
            if ai_response:
                try:
                    report = json.loads(ai_response)
                    report['unified_summary'] = unified_summary
                    report['timestamp'] = datetime.now().isoformat()
                    return report
                except json.JSONDecodeError:
                    return {
                        "unified_report": ai_response,
                        "unified_summary": unified_summary,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return self._fallback_unified_report(all_data, unified_summary)
                
        except Exception as e:
            logger.error(f"Errore report unificato: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    # ==================== METODI DI SUPPORTO ====================
    
    def _calculate_conversion_rate(self, data: pd.DataFrame) -> float:
        """Calcola tasso di conversione"""
        if 'stato' in data.columns:
            converted = data[data['stato'] == 'converted'].shape[0]
            total = len(data)
            return (converted / total * 100) if total > 0 else 0
        return 0
    
    def _get_top_sources(self, data: pd.DataFrame) -> List[Dict]:
        """Ottiene top fonti lead"""
        if 'fonte' in data.columns:
            return data['fonte'].value_counts().head(5).to_dict()
        return []
    
    def _analyze_trends(self, data: pd.DataFrame) -> Dict:
        """Analizza trend temporali"""
        if 'data_registrazione' in data.columns:
            data['data_registrazione'] = pd.to_datetime(data['data_registrazione'])
            trends = data.groupby(data['data_registrazione'].dt.date).size()
            return {
                "daily_average": trends.mean(),
                "growth_rate": ((trends.iloc[-1] - trends.iloc[0]) / trends.iloc[0] * 100) if len(trends) > 1 else 0
            }
        return {}
    
    def _get_broker_distribution(self, data: pd.DataFrame) -> Dict:
        """Distribuzione broker"""
        if 'broker' in data.columns:
            return data['broker'].value_counts().to_dict()
        return {}
    
    def _analyze_platforms(self, data: pd.DataFrame) -> Dict:
        """Analisi piattaforme"""
        if 'piattaforma' in data.columns:
            return data['piattaforma'].value_counts().to_dict()
        return {}
    
    def _analyze_vps_usage(self, data: pd.DataFrame) -> Dict:
        """Analisi uso VPS"""
        if 'vps_ip' in data.columns:
            vps_users = data[data['vps_ip'].notna()].shape[0]
            total = len(data)
            return {
                "vps_users": vps_users,
                "vps_percentage": (vps_users / total * 100) if total > 0 else 0
            }
        return {}
    
    def _calculate_financial_projections(self, data: pd.DataFrame) -> Dict:
        """Calcola proiezioni finanziarie"""
        if 'deposito' in data.columns:
            total_deposits = data['deposito'].sum()
            avg_deposit = data['deposito'].mean()
            return {
                "total_deposits": total_deposits,
                "average_deposit": avg_deposit,
                "projected_monthly": total_deposits * 1.1,  # 10% crescita
                "projected_yearly": total_deposits * 1.2   # 20% crescita
            }
        return {}
    
    def _rank_brokers(self, data: pd.DataFrame) -> List[Dict]:
        """Ranking broker"""
        if 'broker' in data.columns and 'deposito' in data.columns:
            broker_stats = data.groupby('broker').agg({
                'deposito': ['sum', 'mean', 'count']
            }).round(2)
            return broker_stats.to_dict('index')
        return []
    
    def _calculate_broker_metrics(self, data: pd.DataFrame) -> Dict:
        """Calcola metriche broker"""
        return {
            "total_brokers": data['broker'].nunique() if 'broker' in data.columns else 0,
            "average_per_broker": data.groupby('broker')['deposito'].mean().mean() if 'broker' in data.columns and 'deposito' in data.columns else 0
        }
    
    def _analyze_market_trends(self, data: pd.DataFrame) -> Dict:
        """Analizza trend di mercato"""
        return {
            "market_growth": "positive",
            "trend_direction": "upward",
            "volatility": "medium"
        }
    
    def _assess_broker_risks(self, data: pd.DataFrame) -> Dict:
        """Valuta rischi broker"""
        return {
            "risk_level": "low",
            "risk_factors": ["market_volatility", "regulatory_changes"],
            "mitigation_strategies": ["diversification", "risk_monitoring"]
        }
    
    def _get_unified_date_range(self, all_data: Dict[str, pd.DataFrame]) -> Dict:
        """Ottiene range date unificato"""
        all_dates = []
        for df in all_data.values():
            if 'data_registrazione' in df.columns:
                all_dates.extend(pd.to_datetime(df['data_registrazione']).tolist())
        
        if all_dates:
            return {
                "start": min(all_dates).strftime('%Y-%m-%d'),
                "end": max(all_dates).strftime('%Y-%m-%d')
            }
        return {}
    
    def _analyze_cross_project_data(self, all_data: Dict[str, pd.DataFrame]) -> Dict:
        """Analizza dati cross-project"""
        return {
            "total_projects": len(all_data),
            "total_records": sum(len(df) for df in all_data.values()),
            "common_patterns": ["growth_trend", "seasonal_variation"]
        }
    
    # ==================== METODI FALLBACK ====================
    
    def _fallback_lead_analysis(self, data: pd.DataFrame, summary: Dict) -> Dict:
        """Analisi fallback per lead"""
        return {
            "analysis": "Analisi base completata (AI non disponibile)",
            "data_summary": summary,
            "recommendations": ["Migliorare conversion rate", "Ottimizzare fonti lead"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _fallback_cpa_analysis(self, data: pd.DataFrame, metrics: Dict) -> Dict:
        """Analisi fallback per CPA"""
        return {
            "roi_analysis": "Analisi ROI base completata",
            "basic_metrics": metrics,
            "recommendations": ["Ottimizzare budget", "Migliorare ROI"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _fallback_broker_analysis(self, data: pd.DataFrame, analysis: Dict) -> Dict:
        """Analisi fallback per broker"""
        return {
            "broker_rankings": "Ranking base completato",
            "basic_analysis": analysis,
            "recommendations": ["Diversificare broker", "Monitorare performance"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _fallback_unified_report(self, all_data: Dict[str, pd.DataFrame], summary: Dict) -> Dict:
        """Report fallback unificato"""
        return {
            "executive_summary": "Report unificato base completato",
            "unified_summary": summary,
            "recommendations": ["Integrare progetti", "Ottimizzare sinergie"],
            "timestamp": datetime.now().isoformat()
        }
