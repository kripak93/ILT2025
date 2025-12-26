# 🚀 Streamlit Cloud Deployment - Quick Checklist

## ✅ Files Fixed (Ready to Deploy)

### 1. Updated `requirements.txt`
Added missing dependencies:
- `google-generativeai>=0.3.0` - For Gemini AI features
- `python-dotenv>=1.0.0` - For environment variables

### 2. Created `.streamlit/config.toml`
- Theme and server configuration added
- Ready for Streamlit Cloud

### 3. Created `.streamlit/secrets.toml.example`
- Example secrets file for reference

---

## 📝 Streamlit Cloud Deployment Steps

### Step 1: Push Changes to GitHub
```bash
git add .
git commit -m "Fix deployment dependencies and add Streamlit config"
git push origin main
```

### Step 2: Configure Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your repository: `kripak93/ILT2025`
4. Set **Main file path**: `ai_cricket_manager_dashboard.py`
5. Click **"Advanced settings"**
6. Add your **Secrets** (TOML format):
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```
7. Click **"Deploy!"**

---

## 🔑 Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy the API key
4. Add it to Streamlit Cloud secrets (Step 2.6 above)

---

## 🐛 Common Issues & Solutions

### Issue: "Module not found"
**Solution**: Verify all packages are in `requirements.txt` (already fixed!)

### Issue: "GEMINI_API_KEY not found"
**Solution**: 
- Make sure you added the API key in Streamlit Cloud > App Settings > Secrets
- Format must be: `GEMINI_API_KEY = "your_key"`

### Issue: "File not found: cricket_analytics_data.json"
**Solution**: Ensure the JSON file is committed to your repository

### Issue: App crashes on load
**Solution**: Check Streamlit Cloud logs:
- Click on your app > "Manage app" > "Logs"
- Look for error messages

---

## 🧪 Test Locally First

Before deploying, test the app locally:
```bash
streamlit run ai_cricket_manager_dashboard.py
```

Make sure:
- ✅ JSON file loads successfully
- ✅ All visualizations render
- ✅ AI features work (if you have a local `.env` file with your API key)

---

## 📦 What Gets Deployed

Files needed in your repository:
- ✅ `ai_cricket_manager_dashboard.py` (main app)
- ✅ `cricket_analytics_data.json` (data)
- ✅ `requirements.txt` (dependencies - FIXED!)
- ✅ `.streamlit/config.toml` (config - ADDED!)
- ✅ `.streamlit/secrets.toml.example` (reference - ADDED!)

Files NOT needed (stay local):
- ❌ `.env` (use Streamlit Cloud secrets instead)
- ❌ `.streamlit/secrets.toml` (use Streamlit Cloud UI)
- ❌ `__pycache__/` (automatically ignored)
- ❌ `.venv/` (cloud builds its own)

---

## 🎯 Quick Deploy Command

```bash
# 1. Commit and push
git add requirements.txt .streamlit/
git commit -m "Add deployment configuration"
git push origin main

# 2. Then go to share.streamlit.io and follow Step 2 above
```

---

## 🆘 Need Help?

If deployment fails, check:
1. **Streamlit Cloud Logs** - Most informative error messages
2. **GitHub repo** - All files committed and pushed?
3. **Secrets** - API key added correctly in TOML format?
4. **Requirements** - All dependencies listed?

Your app should now deploy successfully! 🎉
