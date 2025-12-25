import streamlit as st
import pandas as pd
import json
import google.generativeai as genai
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AI Cricket Manager Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Configure Gemini
def configure_gemini():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found in environment variables!")
        st.info("Please add your Gemini API key to the .env file")
        st.stop()
    genai.configure(api_key=api_key)

configure_gemini()

# Load data
@st.cache_data
def load_cricket_data():
    try:
        with open('cricket_analytics_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Data file not found!")
        return None

# Function to get AI insights
def get_ai_insights(prompt, context_data):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        full_prompt = f"""
        As an expert cricket analyst and team manager, analyze the following data and provide insights:
        
        Context Data:
        {json.dumps(context_data, indent=2)}
        
        Question/Request:
        {prompt}
        
        Provide detailed, actionable insights with specific recommendations.
        """
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating insights: {str(e)}"

# Main app
def main():
    st.title("🏏 AI Cricket Manager Dashboard")
    st.markdown("### Powered by Google Gemini AI")
    
    # Load data
    data = load_cricket_data()
    if not data:
        return
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Quick Actions")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.header("📊 Dashboard Info")
        st.info("This dashboard uses AI to provide insights on cricket team performance, player statistics, and match strategies.")
        
        st.markdown("---")
        st.header("🤖 AI Model")
        st.write("**Model:** Gemini 2.0 Flash Exp")
        st.write("**Purpose:** Cricket Analytics")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Team Overview", "👥 Player Analysis", "🎯 Match Insights", "🤖 AI Assistant"])
    
    # Tab 1: Team Overview
    with tab1:
        st.header("Team Performance Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Matches", data['team_stats']['total_matches'])
        with col2:
            st.metric("Wins", data['team_stats']['wins'])
        with col3:
            st.metric("Win Rate", f"{data['team_stats']['win_rate']}%")
        with col4:
            st.metric("Avg Score", data['team_stats']['average_score'])
        
        # Recent form
        st.subheader("Recent Form")
        recent_matches = pd.DataFrame(data['recent_matches'])
        st.dataframe(recent_matches, use_container_width=True)
        
        # Get AI insights for team overview
        if st.button("🤖 Get AI Insights on Team Performance", key="team_insights"):
            with st.spinner("Analyzing team performance..."):
                insights = get_ai_insights(
                    "Analyze the team's overall performance, recent form, and provide recommendations for improvement.",
                    {
                        "team_stats": data['team_stats'],
                        "recent_matches": data['recent_matches']
                    }
                )
                st.markdown("### 🎯 AI Insights")
                st.write(insights)
    
    # Tab 2: Player Analysis
    with tab2:
        st.header("Player Performance Analysis")
        
        players_df = pd.DataFrame(data['players'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top batsmen
            st.subheader("🏏 Top Batsmen")
            batsmen = players_df.nlargest(5, 'batting_average')[['name', 'batting_average', 'strike_rate']]
            st.dataframe(batsmen, use_container_width=True)
            
            # Batting average chart
            fig_batting = px.bar(
                batsmen,
                x='name',
                y='batting_average',
                title='Top 5 Batsmen by Average',
                color='batting_average',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_batting, use_container_width=True)
        
        with col2:
            # Top bowlers
            st.subheader("⚡ Top Bowlers")
            bowlers = players_df.nlargest(5, 'wickets')[['name', 'wickets', 'bowling_average', 'economy']]
            st.dataframe(bowlers, use_container_width=True)
            
            # Wickets chart
            fig_bowling = px.bar(
                bowlers,
                x='name',
                y='wickets',
                title='Top 5 Bowlers by Wickets',
                color='wickets',
                color_continuous_scale='Plasma'
            )
            st.plotly_chart(fig_bowling, use_container_width=True)
        
        # Player selector for detailed analysis
        st.subheader("🔍 Detailed Player Analysis")
        selected_player = st.selectbox("Select a player", players_df['name'].tolist())
        
        if st.button("🤖 Get AI Insights on Selected Player", key="player_insights"):
            player_data = players_df[players_df['name'] == selected_player].to_dict('records')[0]
            with st.spinner(f"Analyzing {selected_player}'s performance..."):
                insights = get_ai_insights(
                    f"Provide a detailed analysis of {selected_player}'s performance, strengths, weaknesses, and recommendations for improvement.",
                    {"player": player_data}
                )
                st.markdown("### 🎯 AI Insights")
                st.write(insights)
    
    # Tab 3: Match Insights
    with tab3:
        st.header("Match Strategy & Insights")
        
        # Match selector
        matches_df = pd.DataFrame(data['recent_matches'])
        selected_match = st.selectbox(
            "Select a match",
            [f"{m['opponent']} ({m['date']})" for m in data['recent_matches']]
        )
        
        match_index = [f"{m['opponent']} ({m['date']})" for m in data['recent_matches']].index(selected_match)
        match_data = data['recent_matches'][match_index]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Result", match_data['result'])
        with col2:
            st.metric("Our Score", match_data['our_score'])
        with col3:
            st.metric("Opponent Score", match_data['opponent_score'])
        
        if st.button("🤖 Get AI Match Analysis", key="match_insights"):
            with st.spinner("Analyzing match..."):
                insights = get_ai_insights(
                    f"Analyze this match against {match_data['opponent']}. What went well? What could be improved? What strategies should we employ in future matches against similar opponents?",
                    {"match": match_data}
                )
                st.markdown("### 🎯 AI Insights")
                st.write(insights)
    
    # Tab 4: AI Assistant
    with tab4:
        st.header("🤖 AI Cricket Manager Assistant")
        st.markdown("Ask me anything about your team's performance, player statistics, or match strategies!")
        
        # Chat interface
        user_question = st.text_area(
            "Your Question:",
            placeholder="E.g., Which players should I pick for the next match against a strong bowling attack?",
            height=100
        )
        
        if st.button("🚀 Get AI Response", key="ai_assistant"):
            if user_question:
                with st.spinner("Thinking..."):
                    insights = get_ai_insights(user_question, data)
                    st.markdown("### 💡 AI Response")
                    st.write(insights)
            else:
                st.warning("Please enter a question first!")
        
        # Sample questions
        st.markdown("### 💭 Sample Questions")
        sample_questions = [
            "What's our team's strongest playing XI?",
            "Which players are in best form currently?",
            "What strategies should we use against spin bowling?",
            "Who should be our finisher in T20 matches?",
            "Analyze our recent losing streak"
        ]
        
        for i, question in enumerate(sample_questions):
            if st.button(question, key=f"sample_{i}"):
                with st.spinner("Thinking..."):
                    insights = get_ai_insights(question, data)
                    st.markdown("### 💡 AI Response")
                    st.write(insights)

if __name__ == "__main__":
    main()
