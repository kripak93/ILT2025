# Cricket Analytics Dashboard 🏏

An interactive cricket analytics dashboard built with Streamlit that provides comprehensive insights into player performance, bowling statistics, and match analytics.

## Features

- **Interactive Filters**: Filter data by matchup type, player, and specific matchups
- **Key Metrics**: View total players, average strike rate, run rate, and wickets
- **Performance Visualizations**:
  - Top players by strike rate
  - Runs vs wickets scatter plot
  - Bowling speed analysis
  - Dot ball percentage rankings
- **Detailed Statistics Table**: Comprehensive player performance data
- **SWOT Analysis**: Strengths, weaknesses, and opportunities breakdown

## Live Demo

[Link to your deployed Streamlit app will appear here]

## Installation

1. Clone this repository
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Run the app
```bash
streamlit run streamlit_app.py
```

## Deployment on Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and `streamlit_app.py` as the main file
6. Click "Deploy"

## Data Format

The app expects a JSON file named `cricket_analytics_data.json` with the following structure:
- `matchups`: Player performance data organized by matchup types
- SWOT analysis data with categories for strengths, weaknesses, and opportunities

## Technologies Used

- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis

## Author

Created for cricket analytics and performance insights.

## License

MIT License
