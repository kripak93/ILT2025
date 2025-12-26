import streamlit as st

st.title("🏏 Cricket Dashboard - Test")
st.write("If you see this, the deployment works!")
st.success("✅ App is running successfully!")

# Show that data file exists
import os
if os.path.exists('cricket_analytics_data.json'):
    st.info("✅ Data file found!")
else:
    st.error("❌ Data file not found!")
