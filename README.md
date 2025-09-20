# 🎯 **DASHBOARD UNIFICATA - CPA, LEAD, MATH**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

## 📋 **DESCRIZIONE**

Dashboard unificata che combina le funzionalità di tre progetti esistenti:
- **🎯 DASH_GESTIONE_LEAD**: Gestione completa dei lead aziendali
- **💼 Dashboard_Gestione_CPA**: Gestione clienti CPA con broker e incroci
- **🧮 DASH_PROP_BROKER**: Dashboard matematico per broker, prop firm, wallet e PAMM

## 🚀 **CARATTERISTICHE PRINCIPALI**

### **🔐 Sicurezza Avanzata**
- ✅ **Autenticazione Multi-Progetto**: Sistema unificato per tutti i progetti
- ✅ **Hash Password Multipli**: Supporto per bcrypt, SHA256 con salt
- ✅ **Rate Limiting**: Protezione contro attacchi brute force
- ✅ **Row Level Security**: Sicurezza a livello di riga per Supabase
- ✅ **Audit Trail**: Logging completo delle operazioni

### **🗄️ Database Separati**
- ✅ **3 Database Supabase**: Mantiene i dati separati per ogni progetto
- ✅ **Nessun Dato Mischiato**: Ogni progetto mantiene la sua struttura
- ✅ **Backup Automatico**: Sistema di backup integrato
- ✅ **Gestione Errori**: Fallback automatico e recovery

### **🤖 AI Assistant Unificato**
- ✅ **DeepSeek Integration**: AI Assistant per tutti i progetti
- ✅ **Prompt Personalizzati**: Analisi specifiche per ogni progetto
- ✅ **Analisi Cross-Progetto**: Insights che combinano dati di più progetti
- ✅ **Cache Intelligente**: Ottimizzazione delle risposte

### **🎨 UI/UX Unificata**
- ✅ **Design Coerente**: Interfaccia unificata per tutti i progetti
- ✅ **Navigazione Intuitiva**: Switching facile tra progetti
- ✅ **Componenti Riutilizzabili**: Form, tabelle e grafici unificati
- ✅ **Responsive Design**: Ottimizzato per desktop e mobile

## 🏗️ **ARCHITETTURA**

```
DASHBOARD_UNIFICATA/
├── 📁 config/                    # Configurazione unificata sicura
├── 📁 database/                  # Gestori database per tutti i progetti
├── 📁 components/                # Componenti UI riutilizzabili
├── 📁 pages/                     # Pagine specifiche per ogni progetto
├── 📁 utils/                     # Utility comuni
├── 📁 auth/                      # Sistema autenticazione unificato
├── 📁 ai/                        # AI Assistant unificato
├── 📁 assets/                    # Risorse comuni
├── 📄 app.py                     # App principale unificata
├── 📄 requirements.txt           # Dipendenze unificate
└── 📄 .streamlit/secrets.toml    # Secrets per Streamlit Cloud
```

## 🛠️ **INSTALLAZIONE**

### **Prerequisiti**
- Python 3.8+
- Account Supabase (3 progetti)
- Account Streamlit Cloud (per deployment)

### **Setup Locale**

1. **Clona il repository**
```bash
git clone https://github.com/eziocamporeale/Dash_cpa_lead_math.git
cd Dash_cpa_lead_math
```

2. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```

3. **Configura le variabili d'ambiente**
```bash
# Crea file .env
export LEAD_SUPABASE_URL="https://xjjmpurdjqwjomxmqqks.supabase.co"
export LEAD_SUPABASE_KEY="your-lead-key"
export CPA_SUPABASE_URL="https://your-cpa-project.supabase.co"
export CPA_SUPABASE_KEY="your-cpa-key"
export PROP_SUPABASE_URL="https://znkhbkiexrqujqwgzueq.supabase.co"
export PROP_SUPABASE_KEY="your-prop-key"
export DEEPSEEK_API_KEY="your-deepseek-key"
```

4. **Avvia l'applicazione**
```bash
streamlit run app.py
```

### **Deployment su Streamlit Cloud**

1. **Fork del repository** su GitHub
2. **Configura secrets** in Streamlit Cloud:
   - `supabase.lead_url`
   - `supabase.lead_key`
   - `supabase.cpa_url`
   - `supabase.cpa_key`
   - `supabase.prop_url`
   - `supabase.prop_key`
   - `ai.deepseek_api_key`
3. **Deploy** automatico

## 📊 **FUNZIONALITÀ PER PROGETTO**

### **🎯 LEAD MANAGEMENT**
- ✅ Gestione Lead completa (CRUD)
- ✅ Sistema Task Management
- ✅ Sequenze di Contatto automatiche
- ✅ Template Email/SMS
- ✅ Gestione Gruppi Lead
- ✅ Analytics e Reporting
- ✅ AI Assistant per analisi lead

### **💼 CPA MANAGEMENT**
- ✅ Gestione Clienti CPA (CRUD)
- ✅ Gestione Broker
- ✅ Sistema Incroci
- ✅ Wallet Management
- ✅ Transazioni Wallet
- ✅ AI Assistant per analisi CPA
- ✅ Sistema Sicurezza avanzato

### **🧮 PROP BROKER MANAGEMENT**
- ✅ Gestione Broker forex/CFD
- ✅ Gestione Prop Firm
- ✅ Gestione Wallet crypto
- ✅ Pack Copiatori
- ✅ Gruppi PAMM
- ✅ Sistema Incroci avanzato
- ✅ AI Assistant matematico

## 🔧 **CONFIGURAZIONE**

### **Database Supabase**
Ogni progetto mantiene il suo database Supabase separato:
- **LEAD**: `https://xjjmpurdjqwjomxmqqks.supabase.co`
- **CPA**: `https://your-cpa-project.supabase.co`
- **PROP**: `https://znkhbkiexrqujqwgzueq.supabase.co`

### **Sicurezza**
- **RLS**: Row Level Security abilitato su tutte le tabelle
- **Autenticazione**: Sistema unificato con ruoli granulari
- **Crittografia**: Password e dati sensibili sempre crittografati
- **Audit**: Logging completo di tutte le operazioni

## 🧪 **TESTING**

```bash
# Test connessioni database
python test_database_connections.py

# Test configurazione
python -c "from config import get_config; print('✅ Configurazione OK')"

# Test autenticazione
python -c "from auth import test_auth; test_auth()"
```

## 📈 **PERFORMANCE**

- ✅ **Lazy Loading**: Caricamento dati on-demand
- ✅ **Caching**: Cache intelligente per AI e database
- ✅ **Paginazione**: Gestione efficiente di grandi dataset
- ✅ **Ottimizzazione**: Query ottimizzate per Supabase

## 🔒 **SICUREZZA**

- ✅ **Secrets Management**: Chiavi sensibili mai nel codice
- ✅ **Environment Variables**: Configurazione sicura
- ✅ **Streamlit Secrets**: Deployment sicuro su cloud
- ✅ **Audit Automatico**: Controlli di sicurezza integrati

## 📞 **SUPPORTO**

- **Issues**: [GitHub Issues](https://github.com/eziocamporeale/Dash_cpa_lead_math/issues)
- **Documentation**: [Wiki](https://github.com/eziocamporeale/Dash_cpa_lead_math/wiki)
- **Email**: admin@unified.com

## 📄 **LICENZA**

Proprietario: Ezio Camporeale
Tutti i diritti riservati.

## 🔄 **CHANGELOG**

### **v1.0.0** (2025-01-XX)
- ✅ Release iniziale
- ✅ Unificazione di tutti e 3 i progetti
- ✅ Sistema di autenticazione unificato
- ✅ AI Assistant integrato
- ✅ Sicurezza avanzata implementata
- ✅ Deployment su Streamlit Cloud

---

**🎯 Creato da Ezio Camporeale - Dashboard Unificata CPA, LEAD, MATH**
