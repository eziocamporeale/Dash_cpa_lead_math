# 🚀 GUIDA DEPLOYMENT - Dashboard Unificata

## 📋 Panoramica

Questa guida ti aiuterà a deployare la Dashboard Unificata su Streamlit Cloud.

## 🔧 Prerequisiti

- Account GitHub
- Account Streamlit Cloud
- Repository GitHub con il codice della dashboard

## 📝 Passaggi per il Deployment

### 1. **Preparazione Repository**

Assicurati che il repository contenga:
- ✅ `app.py` (file principale)
- ✅ `requirements.txt`
- ✅ `.streamlit/config.toml`
- ✅ `.streamlit/secrets.toml` (con i tuoi secrets)
- ✅ Tutti i moduli Python

### 2. **Configurazione Secrets**

Nel dashboard Streamlit Cloud, configura i seguenti secrets:

```toml
[supabase]
# Progetto LEAD
lead_url = "https://your-lead-project.supabase.co"
lead_key = "your-lead-supabase-key"

# Progetto CPA
cpa_url = "https://your-cpa-project.supabase.co"
cpa_key = "your-cpa-supabase-key"

# Progetto PROP BROKER
prop_url = "https://your-prop-project.supabase.co"
prop_key = "your-prop-supabase-key"

[ai]
# DeepSeek API
deepseek_api_key = "your-deepseek-api-key"
deepseek_api_url = "https://api.deepseek.com/v1/chat/completions"
deepseek_model = "deepseek-chat"

[auth]
# Credenziali admin
admin_username = "admin"
admin_password = "your-secure-password"
manager_username = "manager"
manager_password = "your-secure-password"
viewer_username = "viewer"
viewer_password = "your-secure-password"

[app]
# Configurazione app
app_title = "Dashboard Unificata"
app_icon = "🎯"
theme_color = "#2E86AB"
```

### 3. **Deployment su Streamlit Cloud**

1. **Vai su** [share.streamlit.io](https://share.streamlit.io)
2. **Clicca** "New app"
3. **Seleziona** il tuo repository GitHub
4. **Imposta**:
   - **Main file path**: `app.py`
   - **Branch**: `main`
5. **Clicca** "Deploy!"

### 4. **Configurazione Post-Deployment**

Dopo il deployment:

1. **Vai** nelle impostazioni dell'app
2. **Configura** i secrets nella sezione "Secrets"
3. **Testa** l'applicazione
4. **Configura** il dominio personalizzato (opzionale)

## 🔒 Sicurezza

### **Secrets Management**
- ❌ **NON** committare mai i secrets su GitHub
- ✅ **USA** sempre Streamlit Cloud secrets
- ✅ **ROTA** periodicamente le API keys

### **Autenticazione**
- ✅ **USA** password complesse
- ✅ **ABILITA** autenticazione a due fattori
- ✅ **MONITORA** gli accessi

### **Database**
- ✅ **ABILITA** Row Level Security (RLS)
- ✅ **USA** connessioni sicure
- ✅ **BACKUP** regolari

## 📊 Monitoraggio

### **Logs**
- Monitora i logs di Streamlit Cloud
- Controlla errori e performance
- Configura alert per errori critici

### **Performance**
- Monitora tempi di risposta
- Ottimizza query database
- Usa cache quando possibile

## 🛠️ Troubleshooting

### **Errori Comuni**

#### **ImportError: No module named 'xxx'**
```bash
# Soluzione: Aggiungi il modulo a requirements.txt
pip freeze > requirements.txt
```

#### **Database Connection Error**
```bash
# Soluzione: Verifica secrets Supabase
# Controlla URL e API key
```

#### **Authentication Failed**
```bash
# Soluzione: Verifica credenziali
# Controlla password hash
```

### **Debug Mode**

Per debug locale:
```bash
# Abilita debug mode
export STREAMLIT_DEBUG=true
streamlit run app.py
```

## 📈 Ottimizzazioni

### **Performance**
- Usa `@st.cache_data` per cache
- Ottimizza query database
- Riduci dimensioni immagini

### **UX**
- Implementa loading states
- Aggiungi error handling
- Ottimizza mobile experience

## 🔄 Aggiornamenti

### **Deploy Nuove Versioni**
1. **Push** su GitHub
2. **Streamlit** auto-deploy
3. **Testa** la nuova versione
4. **Monitora** per errori

### **Rollback**
1. **Vai** nelle impostazioni app
2. **Seleziona** versione precedente
3. **Ripristina** deployment

## 📞 Supporto

Per problemi:
- 📧 Email: support@example.com
- 📱 Telegram: @your_telegram
- 🐛 Issues: GitHub Issues

---

**Creato da Ezio Camporeale** 🚀
