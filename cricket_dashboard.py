import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Load the JSON data
with open(r'c:\Users\kripa\Documents\Downloads\cricket_analytics_data (1).json', 'r') as f:
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

# Initialize the Dash app with a Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Cricket Analytics Dashboard", className="text-center mb-4 mt-4"),
            html.Hr()
        ])
    ]),
    
    # Filters Row
    dbc.Row([
        dbc.Col([
            html.Label("Select Matchup Type:"),
            dcc.Dropdown(
                id='type-filter',
                options=[{'label': t, 'value': t} for t in df['Type'].unique()],
                value=df['Type'].unique()[0] if len(df['Type'].unique()) > 0 else None,
                clearable=False
            )
        ], md=4),
        dbc.Col([
            html.Label("Select Player:"),
            dcc.Dropdown(
                id='player-filter',
                options=[{'label': p, 'value': p} for p in sorted(df['Player'].unique())],
                value=None,
                placeholder="All Players"
            )
        ], md=4),
        dbc.Col([
            html.Label("Select Matchup:"),
            dcc.Dropdown(
                id='matchup-filter',
                options=[{'label': m, 'value': m} for m in sorted(df['Matchup'].unique())],
                value=None,
                placeholder="All Matchups"
            )
        ], md=4),
    ], className="mb-4"),
    
    # Key Metrics Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Players", className="card-title"),
                    html.H2(id="total-players", className="text-primary")
                ])
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg Strike Rate", className="card-title"),
                    html.H2(id="avg-sr", className="text-success")
                ])
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg Run Rate", className="card-title"),
                    html.H2(id="avg-rr", className="text-info")
                ])
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Wickets", className="card-title"),
                    html.H2(id="total-wkts", className="text-danger")
                ])
            ])
        ], md=3),
    ], className="mb-4"),
    
    # Visualizations Row 1
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='strike-rate-chart')
        ], md=6),
        dbc.Col([
            dcc.Graph(id='runs-wickets-scatter')
        ], md=6),
    ], className="mb-4"),
    
    # Visualizations Row 2
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bowling-speed-chart')
        ], md=6),
        dbc.Col([
            dcc.Graph(id='dot-percentage-chart')
        ], md=6),
    ], className="mb-4"),
    
    # Visualizations Row 3
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='player-performance-table')
        ], md=12),
    ], className="mb-4"),
    
    # SWOT Analysis Section
    dbc.Row([
        dbc.Col([
            html.H3("SWOT Analysis", className="mt-4 mb-3"),
            html.Div(id='swot-analysis')
        ])
    ], className="mb-4"),
    
], fluid=True)

# Callbacks
@callback(
    [Output('total-players', 'children'),
     Output('avg-sr', 'children'),
     Output('avg-rr', 'children'),
     Output('total-wkts', 'children')],
    [Input('type-filter', 'value'),
     Input('player-filter', 'value'),
     Input('matchup-filter', 'value')]
)
def update_metrics(type_val, player_val, matchup_val):
    filtered_df = df.copy()
    
    if type_val:
        filtered_df = filtered_df[filtered_df['Type'] == type_val]
    if player_val:
        filtered_df = filtered_df[filtered_df['Player'] == player_val]
    if matchup_val:
        filtered_df = filtered_df[filtered_df['Matchup'] == matchup_val]
    
    total_players = filtered_df['Player'].nunique()
    avg_sr = f"{filtered_df['SR'].mean():.2f}" if 'SR' in filtered_df.columns and len(filtered_df) > 0 else "N/A"
    avg_rr = f"{filtered_df['RR'].mean():.2f}" if 'RR' in filtered_df.columns and len(filtered_df) > 0 else "N/A"
    total_wkts = int(filtered_df['Wks'].sum()) if 'Wks' in filtered_df.columns and len(filtered_df) > 0 else 0
    
    return total_players, avg_sr, avg_rr, total_wkts

@callback(
    Output('strike-rate-chart', 'figure'),
    [Input('type-filter', 'value'),
     Input('player-filter', 'value'),
     Input('matchup-filter', 'value')]
)
def update_strike_rate_chart(type_val, player_val, matchup_val):
    filtered_df = df.copy()
    
    if type_val:
        filtered_df = filtered_df[filtered_df['Type'] == type_val]
    if player_val:
        filtered_df = filtered_df[filtered_df['Player'] == player_val]
    if matchup_val:
        filtered_df = filtered_df[filtered_df['Matchup'] == matchup_val]
    
    # Get top 15 players by strike rate
    if 'SR' in filtered_df.columns and len(filtered_df) > 0:
        top_players = filtered_df.nlargest(15, 'SR')
        fig = px.bar(top_players, x='Player', y='SR', 
                     title='Top 15 Players by Strike Rate',
                     labels={'SR': 'Strike Rate', 'Player': 'Player Name'},
                     color='SR',
                     color_continuous_scale='Viridis')
        fig.update_layout(xaxis_tickangle=-45)
    else:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
    
    return fig

@callback(
    Output('runs-wickets-scatter', 'figure'),
    [Input('type-filter', 'value'),
     Input('player-filter', 'value'),
     Input('matchup-filter', 'value')]
)
def update_runs_wickets_scatter(type_val, player_val, matchup_val):
    filtered_df = df.copy()
    
    if type_val:
        filtered_df = filtered_df[filtered_df['Type'] == type_val]
    if player_val:
        filtered_df = filtered_df[filtered_df['Player'] == player_val]
    if matchup_val:
        filtered_df = filtered_df[filtered_df['Matchup'] == matchup_val]
    
    if 'Runs' in filtered_df.columns and 'Wks' in filtered_df.columns and len(filtered_df) > 0:
        fig = px.scatter(filtered_df, x='Runs', y='Wks', 
                        hover_data=['Player'], 
                        title='Runs vs Wickets',
                        labels={'Runs': 'Total Runs Conceded', 'Wks': 'Wickets Taken'},
                        color='Ave' if 'Ave' in filtered_df.columns else None,
                        size='BF' if 'BF' in filtered_df.columns else None)
    else:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
    
    return fig

@callback(
    Output('bowling-speed-chart', 'figure'),
    [Input('type-filter', 'value'),
     Input('player-filter', 'value'),
     Input('matchup-filter', 'value')]
)
def update_bowling_speed_chart(type_val, player_val, matchup_val):
    filtered_df = df.copy()
    
    if type_val:
        filtered_df = filtered_df[filtered_df['Type'] == type_val]
    if player_val:
        filtered_df = filtered_df[filtered_df['Player'] == player_val]
    if matchup_val:
        filtered_df = filtered_df[filtered_df['Matchup'] == matchup_val]
    
    if 'Ave kph' in filtered_df.columns and len(filtered_df) > 0:
        # Get top 15 by average speed
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
            title='Bowling Speed Analysis (Top 15)',
            xaxis_title='Player',
            yaxis_title='Speed (kph)',
            xaxis_tickangle=-45,
            barmode='group'
        )
    else:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
    
    return fig

@callback(
    Output('dot-percentage-chart', 'figure'),
    [Input('type-filter', 'value'),
     Input('player-filter', 'value'),
     Input('matchup-filter', 'value')]
)
def update_dot_percentage_chart(type_val, player_val, matchup_val):
    filtered_df = df.copy()
    
    if type_val:
        filtered_df = filtered_df[filtered_df['Type'] == type_val]
    if player_val:
        filtered_df = filtered_df[filtered_df['Player'] == player_val]
    if matchup_val:
        filtered_df = filtered_df[filtered_df['Matchup'] == matchup_val]
    
    if 'Dot%' in filtered_df.columns and len(filtered_df) > 0:
        # Get top 15 by dot percentage
        top_dot = filtered_df.nlargest(15, 'Dot%')
        
        fig = px.bar(top_dot, x='Player', y='Dot%',
                    title='Top 15 Players by Dot Ball Percentage',
                    labels={'Dot%': 'Dot Ball %', 'Player': 'Player Name'},
                    color='Dot%',
                    color_continuous_scale='RdYlGn')
        fig.update_layout(xaxis_tickangle=-45)
    else:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
    
    return fig

@callback(
    Output('player-performance-table', 'figure'),
    [Input('type-filter', 'value'),
     Input('player-filter', 'value'),
     Input('matchup-filter', 'value')]
)
def update_performance_table(type_val, player_val, matchup_val):
    filtered_df = df.copy()
    
    if type_val:
        filtered_df = filtered_df[filtered_df['Type'] == type_val]
    if player_val:
        filtered_df = filtered_df[filtered_df['Player'] == player_val]
    if matchup_val:
        filtered_df = filtered_df[filtered_df['Matchup'] == matchup_val]
    
    # Select key columns for the table
    display_columns = ['Player', 'Span', 'Mat', 'Inns', 'Runs', 'BF', 'SR', 'Wks', 'Ave', 'RR', 'Dot%']
    available_columns = [col for col in display_columns if col in filtered_df.columns]
    
    if len(filtered_df) > 0 and len(available_columns) > 0:
        table_df = filtered_df[available_columns].head(20)
        
        # Round numeric columns
        for col in table_df.columns:
            if table_df[col].dtype in ['float64', 'float32']:
                table_df[col] = table_df[col].round(2)
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=list(table_df.columns),
                fill_color='paleturquoise',
                align='left',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=[table_df[col] for col in table_df.columns],
                fill_color='lavender',
                align='left',
                font=dict(size=11)
            )
        )])
        
        fig.update_layout(
            title='Player Performance Details (Top 20)',
            height=500
        )
    else:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
    
    return fig

@callback(
    Output('swot-analysis', 'children'),
    [Input('type-filter', 'value')]
)
def update_swot_analysis(type_val):
    if len(swot_df) == 0:
        return html.P("No SWOT analysis data available")
    
    swot_cards = []
    
    for swot_type in ['strength', 'weakness', 'opportunity']:
        type_data = swot_df[swot_df['Type'] == swot_type]
        
        if len(type_data) > 0:
            color_map = {
                'strength': 'success',
                'weakness': 'danger',
                'opportunity': 'info'
            }
            
            cards = []
            for _, row in type_data.iterrows():
                cards.append(
                    dbc.Card([
                        dbc.CardHeader(row['Category']),
                        dbc.CardBody([
                            html.P(row['Description']),
                            html.P(row['Text'], className='text-muted small')
                        ])
                    ], color=color_map.get(swot_type, 'secondary'), outline=True, className='mb-2')
                )
            
            swot_cards.append(
                dbc.Col([
                    html.H5(swot_type.capitalize() + 's', className='mb-3'),
                    html.Div(cards)
                ], md=4)
            )
    
    if len(swot_cards) > 0:
        return dbc.Row(swot_cards)
    else:
        return html.P("No SWOT analysis data available")

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
