# 🚀 Deployment to Streamlit Cloud

## Quick Deploy Steps

### 1. Fork/Push Repository

Make sure your code is on GitHub in a public or private repository.

### 2. Go to Streamlit Cloud

1. Visit: https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"

### 3. Configure App

- **Repository**: Select your `Explosive_stock` repo
- **Branch**: `claude/penny-stock-detector-01RYNw7sfdA6kmzFqjjRPRXW` (or your main branch)
- **Main file path**: `app.py`

### 4. Add Secrets (IMPORTANT!)

Click on "Advanced settings" → "Secrets"

Paste this configuration (with your real API key):

```toml
FMP_API_KEY = "your_real_fmp_api_key_here"

# Optional overrides
MIN_PRICE = 0.50
MAX_PRICE = 10.0
MAX_MARKET_CAP = 300000000
MIN_VOLUME = 100000
```

### 5. Deploy!

Click "Deploy" and wait ~1-2 minutes.

---

## Configuration Priority

The app loads configuration in this order:

1. **Streamlit Secrets** (cloud deployment) - highest priority
2. **config.py** (local development) - fallback
3. **Default values** (hardcoded) - if nothing else exists

This means:
- ✅ Works on Streamlit Cloud with secrets
- ✅ Works locally with config.py
- ✅ Works everywhere with sensible defaults

---

## Local Development with Secrets

If you want to use secrets locally instead of `config.py`:

```bash
# Create secrets file
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit with your API key
nano .streamlit/secrets.toml
```

**Note**: `.streamlit/secrets.toml` is in `.gitignore` and won't be committed.

---

## Troubleshooting

### "No API key" error
→ Add `FMP_API_KEY` to Streamlit Cloud secrets

### App crashes on startup
→ Check logs in Streamlit Cloud dashboard
→ Verify secrets are properly formatted (TOML syntax)

### Slow loading
→ Should only take 1-2 minutes with optimized requirements.txt
→ Check if dependencies installed successfully in logs

---

## Performance Tips

### Caching
The app uses `@st.cache_resource` for the screener instance.
This means subsequent scans are faster.

### Rate Limiting
FMP API has rate limits depending on your plan:
- **Free**: 250 requests/day
- **Starter**: 300 requests/minute
- **Professional**: 750 requests/minute

Adjust `max_stocks` in the UI if you hit rate limits.

---

## Custom Domain (Optional)

Once deployed, you can:
1. Go to app settings
2. Add a custom domain
3. Point your DNS to Streamlit Cloud

---

**Your app URL will be:**
`https://your-app-name.streamlit.app`

Share it and start detecting explosive penny stocks! 🚀
