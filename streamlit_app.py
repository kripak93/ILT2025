import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Page config
st.set_page_config(
    page_title="Cricket Analytics Dashboard",
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
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the JSON data
@st.cache_data
def load_data():
    with open('cricket_analytics_data.json', 'r') as f:
        data = json.load(f)
    
    # Extract matchups data into a pandas DataFrame
    all_matchup_data = []
    for matchup_name, matchup_info in data.get('matchups', {}).items():
        matchup_type = matchup_info.get('type', 'unknown')
        for record in matchup_info.get('data', []):
            record_copy = record.copy()
            record_copy['Matchup'] = matchup_name
            record_copy['Type'] = matchup_type
            all_matchup_data.append(record_copy)
    
    df = pd.DataFrame(all_matchup_data)
    
    # Extract SWOT analysis data
    swot_data = []
    for key, value in data.items():
        if key not in ['teams', 'matchups']:
            if isinstance(value, dict) and 'type' in value:
                swot_data.append({
                    'Category': key,
                    'Type': value['type'],
                    'Description': value.get('description', ''),
                    'Text': value.get('text', '')
                })
    
    swot_df = pd.DataFrame(swot_data)
    
    return df, swot_df

# Load data
df, swot_df = load_data()

# Header
st.title("🏏 Cricket Analytics Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("Filters")

# Type filter
type_options = ['All'] + list(df['Type'].unique())
selected_type = st.sidebar.selectbox("Select Matchup Type", type_options)

# Player filter
player_options = ['All'] + sorted(df['Player'].unique().tolist())
selected_player = st.sidebar.selectbox("Select Player", player_options)

# Matchup filter
matchup_options = ['All'] + sorted(df['Matchup'].unique().tolist())
selected_matchup = st.sidebar.selectbox("Select Matchup", matchup_options)

# Apply filters
filtered_df = df.copy()

if selected_type != 'All':
    filtered_df = filtered_df[filtered_df['Type'] == selected_type]

if selected_player != 'All':
    filtered_df = filtered_df[filtered_df['Player'] == selected_player]

if selected_matchup != 'All':
    filtered_df = filtered_df[filtered_df['Matchup'] == selected_matchup]

# Key Metrics
st.header("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_players = filtered_df['Player'].nunique()
    st.metric("Total Players", total_players)

with col2:
    avg_sr = filtered_df['SR'].mean() if 'SR' in filtered_df.columns and len(filtered_df) > 0 else 0
    st.metric("Avg Strike Rate", f"{avg_sr:.2f}")

with col3:
    avg_rr = filtered_df['RR'].mean() if 'RR' in filtered_df.columns and len(filtered_df) > 0 else 0
    st.metric("Avg Run Rate", f"{avg_rr:.2f}")

with col4:
    total_wkts = int(filtered_df['Wks'].sum()) if 'Wks' in filtered_df.columns and len(filtered_df) > 0 else 0
    st.metric("Total Wickets", total_wkts)

st.markdown("---")

# Visualizations
st.header("Performance Analysis")

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 15 Players by Strike Rate")
    if 'SR' in filtered_df.columns and len(filtered_df) > 0:
        top_players = filtered_df.nlargest(15, 'SR')
        fig = px.bar(top_players, x='Player', y='SR',
                     labels={'SR': 'Strike Rate', 'Player': 'Player Name'},
                     color='SR',
                     color_continuous_scale='Viridis')
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for this selection")

with col2:
    st.subheader("Runs vs Wickets")
    if 'Runs' in filtered_df.columns and 'Wks' in filtered_df.columns and len(filtered_df) > 0:
        fig = px.scatter(filtered_df, x='Runs', y='Wks',
                        hover_data=['Player'],
                        labels={'Runs': 'Total Runs Conceded', 'Wks': 'Wickets Taken'},
                        color='Ave' if 'Ave' in filtered_df.columns else None,
                        size='BF' if 'BF' in filtered_df.columns else None)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for this selection")

# Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Bowling Speed Analysis")
    if 'Ave kph' in filtered_df.columns and len(filtered_df) > 0:
        top_bowlers = filtered_df.nlargest(15, 'Ave kph')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Average Speed',
            x=top_bowlers['Player'],
            y=top_bowlers['Ave kph'],
            marker_color='lightblue'
        ))
        
        if 'Max kph' in top_bowlers.columns:
            fig.add_trace(go.Scatter(
                name='Max Speed',
                x=top_bowlers['Player'],
                y=top_bowlers['Max kph'],
                mode='markers',
                marker=dict(size=10, color='red', symbol='diamond')
            ))
        
        fig.update_layout(
            xaxis_title='Player',
            yaxis_title='Speed (kph)',
            xaxis_tickangle=-45,
            height=400,
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for this selection")

with col2:
    st.subheader("Top 15 by Dot Ball Percentage")
    if 'Dot%' in filtered_df.columns and len(filtered_df) > 0:
        top_dot = filtered_df.nlargest(15, 'Dot%')
        
        fig = px.bar(top_dot, x='Player', y='Dot%',
                    labels={'Dot%': 'Dot Ball %', 'Player': 'Player Name'},
                    color='Dot%',
                    color_continuous_scale='RdYlGn')
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for this selection")

st.markdown("---")

# Performance Table
st.header("Detailed Performance Statistics")

display_columns = ['Player', 'Span', 'Mat', 'Inns', 'Runs', 'BF', 'SR', 'Wks', 'Ave', 'RR', 'Dot%']
available_columns = [col for col in display_columns if col in filtered_df.columns]

if len(filtered_df) > 0 and len(available_columns) > 0:
    table_df = filtered_df[available_columns].head(20).copy()
    
    # Round numeric columns
    for col in table_df.columns:
        if table_df[col].dtype in ['float64', 'float32']:
            table_df[col] = table_df[col].round(2)
    
    st.dataframe(table_df, use_container_width=True, height=400)
else:
    st.info("No data available for this selection")

st.markdown("---")

# SWOT Analysis
if len(swot_df) > 0:
    st.header("SWOT Analysis")
    
    # Create tabs for different SWOT types
    swot_types = swot_df['Type'].unique()
    
    if len(swot_types) > 0:
        tabs = st.tabs([t.capitalize() + 's' for t in ['strength', 'weakness', 'opportunity'] if t in swot_types])
        
        tab_idx = 0
        for swot_type in ['strength', 'weakness', 'opportunity']:
            if swot_type in swot_types:
                with tabs[tab_idx]:
                    type_data = swot_df[swot_df['Type'] == swot_type]
                    
                    for _, row in type_data.iterrows():
                        with st.expander(row['Category']):
                            st.write(f"**Description:** {row['Description']}")
                            st.write(f"**Details:** {row['Text']}")
                
                tab_idx += 1

# Footer
st.markdown("---")
st.markdown("### 📊 Cricket Analytics Dashboard | Data-driven insights for cricket performance analysis")
