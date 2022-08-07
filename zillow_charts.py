# An app that displays the latest housing data from Zillow

# Imports -----------------
from turtle import color
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
inventory = pd.read_csv('Metro_invt_fs_uc_sfrcondo_week.csv') # Home Inventory 
list_sale_price = pd.read_csv('Metro_median_sale_price_uc_sfrcondo_week.csv') # List and Sale Prices
list_to_sale = pd.read_csv('Metro_mean_sale_to_list_uc_sfrcondo_week.csv') # Mean sale to list ratio
price_cuts = pd.read_csv('Metro_perc_listings_price_cut_uc_sfrcondo_week.csv') # Price Cuts
percent_below_list = pd.read_csv('Metro_pct_sold_below_list_uc_sfrcondo_week.csv') # Percent of Home Sold below List Price
rent = pd.read_csv('Metro_ZORI_AllHomesPlusMultifamily_Smoothed.csv') # Rental Prices

# Data Transforms
home_pricesT = dt.home_price_transform(home_prices)
inventoryT = dt.home_price_transform(inventory)
list_sale_priceT = dt.home_price_transform(list_sale_price)
list_to_saleT = dt.home_price_transform(list_to_sale)
price_cutsT = dt.home_price_transform(price_cuts)
percent_below_listT = dt.home_price_transform(percent_below_list)
rentT = dt.home_rent_transform(rent)

# App ----------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.layout = dbc.Container(
    [
        html.P(style={'margin': 10}),
        html.H1('Housing Market Trends', style={'backgroundColor':'white', 'textAlign': 'center'}),
        #html.Hr(style={'height': 2}),
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
        html.H2('Sale Price'),
        dbc.Row(dcc.Graph(id='list_price_graph')), # List Price Graph
        html.H2('Sale to List Ratio'),
        dbc.Row(dcc.Graph(id='list_to_sale_graph')), # List to Sale Graph
        html.H2('Price Cut'),
        dbc.Row(dcc.Graph(id='price_cut_graph')), # Price Cut Graph
        html.H2('Percent of Homes that Sold Below List Price'),
        dbc.Row(dcc.Graph(id='percent_below_list_graph')), # Percent below list
        html.H2('Rent'),
        dbc.Row(dcc.Graph(id='rent_graph')), # Rental Rates Graph
        html.H6([
            "Made possible thanks to Zillow's public data @ ",
            html.A("https://www.zillow.com/research/data/", href='https://www.zillow.com/research/data/')
        ]), 
        
        
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
    fig.update_layout(title='Zillow Home Value Index - i.e. the typical home value for each region',
                   xaxis_title='Date',
                   yaxis_title='Home Value ($)',
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
                   xaxis_title='Date',
                   yaxis_title='Number of Homes for Sale',
                   height=600,)
    return fig

# Callback for Sale Price
@app.callback(
    Output(component_id='list_price_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = list_sale_priceT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Median Sale Price (All homes, weekly)',
                   xaxis_title='Date',
                   yaxis_title='Price ($)',
                   height=600,)
    return fig

# Callback for List to Sale
@app.callback(
    Output(component_id='list_to_sale_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = list_to_saleT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Mean Sale to List Ratio (All homes, weekly)',
                   xaxis_title='Date',
                   yaxis_title='Sale to List',
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
    fig.update_layout(title='Share of Listings with a Price Cut (All home types)',
                   xaxis_title='Date',
                   yaxis_title='Percent of Homes with a Price Cut (%)',
                   height=600,)
    return fig  

# Percent of Homes Sold Below the List Price
@app.callback(
    Output(component_id='percent_below_list_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = percent_below_listT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Percent of Homes Sold Below the List Price',
                   xaxis_title='Date',
                   yaxis_title='Percent of Homes Sold below List (%)',
                   height=600,)
    return fig   

# Callback for Rental Rates
@app.callback(
    Output(component_id='rent_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = rentT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Monthly Rental Rate per Region',
                   xaxis_title='Date',
                   yaxis_title='Rental Rate ($)',
                   height=600,)
    return fig 

if __name__ == '__main__':
    app.run_server(debug=True)