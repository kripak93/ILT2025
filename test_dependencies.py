"""
Test script to verify all required dependencies can be imported
This validates that requirements.txt includes all necessary packages
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports from ai_cricket_manager_dashboard.py...")
    
    try:
        import streamlit
        print("✓ streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import streamlit: {e}")
        return False
    
    try:
        import pandas
        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pandas: {e}")
        return False
    
    try:
        import plotly.express
        import plotly.graph_objects
        from plotly.subplots import make_subplots
        print("✓ plotly imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import plotly: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import dotenv: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✓ google-generativeai imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import google.generativeai: {e}")
        return False
    
    print("\n✅ All required dependencies are available!")
    return True

if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)
