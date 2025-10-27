import pandas as pd
from pathlib import Path
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


data_file = Path(__file__).parent.parent / "pink_morsel_sales.csv"
df = pd.read_csv(data_file)
df['date'] = pd.to_datetime(df['date'])


app = Dash(__name__)


app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={'textAlign': 'center', 'color': '#2C3E50', 'marginBottom': '20px'}
        ),
        
        html.Div(
            [
                html.Label("Select Region:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
                dcc.RadioItems(
                    id='region-selector',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'}
                    ],
                    value='all',
                    labelStyle={'display': 'inline-block', 'marginRight': '15px'},
                    inputStyle={'marginRight': '5px'}
                )
            ],
            style={'textAlign': 'center', 'marginBottom': '30px'}
        ),
        
        dcc.Graph(id='sales-graph')
    ],
    style={'fontFamily': 'Arial, sans-serif', 'margin': '50px'}
)


@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-selector', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['region'].str.lower() == selected_region]
    
    
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    
    
    fig = px.line(
        daily_sales,
        x='date',
        y='sales',
        title=f"Pink Morsel Sales - {selected_region.capitalize()} Region",
        labels={'date': 'Date', 'sales': 'Total Sales ($)'},
        markers=True
    )
    
    
    fig.update_layout(
        title={'x':0.5, 'xanchor':'center'},
        plot_bgcolor='#F9F9F9',
        paper_bgcolor='#F9F9F9',
        font={'color': '#34495E', 'size': 14}
    )
    fig.update_traces(line=dict(color='#E74C3C', width=3))
    
    return fig


if __name__ == "__main__":
    print("🚀 Dash app starting! Open http://127.0.0.1:8050/ in your browser")
    app.run(debug=False, host="127.0.0.1", port=8050)
