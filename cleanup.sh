#!/bin/bash
echo "🧹 Cleaning up repository for AI Cricket Manager Dashboard..."
git rm cricket_dashboard.py
git rm streamlit_app.py  
git rm app.py
git rm requirements.txt
git rm streamlit_requirements.txt
git rm test_data_structure.py
git rm DEPLOYMENT_CHECKLIST.md
git rm deploy_streamlit_cloud.md
echo "✅ Files marked for deletion"
git mv requirements_deployment.txt requirements.txt
echo "✅ Renamed requirements_deployment.txt to requirements.txt"
git commit -m "Clean up: Remove old files and keep only AI Cricket Manager Dashboard essentials"
echo "🚀 Ready to push. Run: git push origin main"