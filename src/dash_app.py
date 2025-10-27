import pandas as pd
from pathlib import Path
from dash import Dash, dcc, html
import plotly.express as px

# --- Load Data ---
data_file = Path(__file__).parent.parent / "pink_morsel_sales.csv"
df = pd.read_csv(data_file)

df['date'] = pd.to_datetime(df['date'])

df = df.sort_values('date')

daily_sales = df.groupby('date')['sales'].sum().reset_index()

# --- Create Line Chart ---

fig = px.line(
    daily_sales,
    x='date',
    y='sales',
    title='Daily Pink Morsel Sales',
    labels={'date': 'Date', 'sales': 'Total Sales ($)'}
)



# --- Build Dash App ---
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Pink Morsel Sales Visualiser", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])


if __name__ == "__main__":
    print("Dash app starting! Open http://127.0.0.1:8050/ in your browser")
    app.run(debug=False, host="127.0.0.1", port=8050)


