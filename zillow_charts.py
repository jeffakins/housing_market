# An app that displays the latest housing data from Zillow

# Imports -----------------
import pandas as pd

import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# Data Imports
import data_transform as dt

# Data ---------------------
# Data Imports
home_prices = pd.read_csv('Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv') # Zillow Home Value Index 
inventory = pd.read_csv('Metro_invt_fs_uc_sfrcondo_sm_month.csv') # Home Inventory 
list_sale_price = pd.read_csv('Metro_mlp_uc_sfrcondo_sm_month.csv') # List and Sale Prices
price_cuts = pd.read_csv('Metro_sales_count_now_uc_sfrcondo_month.csv') # Sales Count and Price Cuts

# Data Transforms
home_pricesT = dt.home_price_transform(home_prices)

# Graphs -------------------

fig = px.line(home_pricesT, x=home_pricesT.index, y=home_pricesT['Los Angeles-Long Beach-Anaheim, CA'])
fig.show()

# App ----------------------

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Life expentancy progression of countries per continents'),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        options=["Asia", "Europe", "Africa","Americas","Oceania"],
        value=["Americas", "Oceania"],
        inline=True
    ),
])


@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"))
def update_line_chart(continents):
    df = px.data.gapminder() # replace with your own data source
    mask = df.continent.isin(continents)
    fig = px.line(df[mask], 
        x="year", y="lifeExp", color='country')
    return fig


app.run_server(debug=True)