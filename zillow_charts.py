# An app that displays the latest housing data from Zillow

# Imports -----------------
import pandas as pd
 # Plotly
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
 # Dash
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
 # Bootstrap
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

 # Data Imports
import data_transform as dt

# Data ---------------------
# Data Imports
home_prices = pd.read_csv('Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv') # Zillow Home Value Index 
inventory = pd.read_csv('Metro_invt_fs_uc_sfrcondo_sm_month.csv') # Home Inventory 
list_sale_price = pd.read_csv('Metro_mlp_uc_sfrcondo_sm_month.csv') # List and Sale Prices
price_cuts = pd.read_csv('Metro_perc_listings_price_cut_uc_sfrcondo_sm_week.csv') # Sales Count and Price Cuts

# Data Transforms
home_pricesT = dt.home_price_transform(home_prices)
inventoryT = dt.home_price_transform(inventory)
list_sale_priceT = dt.home_price_transform(list_sale_price)
price_cutsT = dt.home_price_transform(price_cuts)

# App ----------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.layout = dbc.Container(
    [
        html.H2('Home Prices'),
        dbc.Row(dcc.Dropdown(home_pricesT.columns, 
                    id='city_selection', 
                    value= home_pricesT.columns[1:6],
                    multi=True, 
                    placeholder="Select a city",)
        ),
        html.Div(id='city_output_container'),
        dbc.Row(dcc.Graph(id='home_prices_graph')), # Home Value Graph
        html.H2('Inventory'),
        dbc.Row(dcc.Graph(id='inventory_graph')), # Inventory Graph
        html.H2('List Price'),
        dbc.Row(dcc.Graph(id='list_price_graph')), # List Price Graph
        html.H2('Price Cut'),
        dbc.Row(dcc.Graph(id='price_cut_graph')), # Price Cut Graph
    ],
    fluid=True,
)
# Callback for Home Value Estimate
@app.callback(
    Output(component_id='home_prices_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = home_pricesT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Zillow Home Value Index',
                   xaxis_title='Year',
                   yaxis_title='Home Value',
                   height=600,)
    return fig

# Callback for Inventory Levels
@app.callback(
    Output(component_id='inventory_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = inventoryT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Home Inventory Levels',
                   xaxis_title='Year',
                   yaxis_title='Number of Homes for Sale',
                   height=600,)
    return fig

# Callback for List Price
@app.callback(
    Output(component_id='list_price_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = list_sale_priceT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Median List Price',
                   xaxis_title='Year',
                   yaxis_title='Price',
                   height=600,)
    return fig

# Callback for Price Cuts
@app.callback(
    Output(component_id='price_cut_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = price_cutsT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Mean Price Cut of Homes per Region',
                   xaxis_title='Year',
                   yaxis_title='Price Cut Amount',
                   height=600,)
    return fig    

if __name__ == '__main__':
    app.run_server(debug=True)