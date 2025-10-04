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
home_prices = pd.read_csv('Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv') # Zillow Home Value Index - Smoothed; all homes; seasonally adjusted
inventory = pd.read_csv('Metro_invt_fs_uc_sfrcondo_sm_month.csv') # For Sale Inventory - Smoothed; all homes; weekly
list_sale_price = pd.read_csv('Metro_median_sale_price_uc_sfrcondo_sm_sa_month.csv') # Median Sales Price - Smoothed; all homes; monthly
mean_days_to_pending = pd.read_csv('Metro_mean_doz_pending_uc_sfrcondo_sm_month.csv') # Mean sale to list ratio - Smoothed; all homes; weekly
price_cuts = pd.read_csv('Metro_perc_listings_price_cut_uc_sfrcondo_sm_month.csv') # Share of Listings with a Price cut - smoothed; all homes; weekly
percent_below_list = pd.read_csv('Metro_pct_sold_below_list_uc_sfrcondo_sm_month.csv') # Percent of Home Sold below List Price - smoothed; all homes; weekly
rent = pd.read_csv('Metro_zori_uc_sfrcondomfr_sm_month.csv') # Rental Prices; all homes

zhvi_sfh = pd.read_csv('Metro_zhvi_uc_sfr_tier_0.33_0.67_sm_sa_month.csv')
zhvi_condos = pd.read_csv('Metro_zhvi_uc_condo_tier_0.33_0.67_sm_sa_month.csv')
zhvi_1bdr = pd.read_csv('Metro_zhvi_bdrmcnt_1_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')
zhvi_2bdr = pd.read_csv('Metro_zhvi_bdrmcnt_2_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')
zhvi_3bdr = pd.read_csv('Metro_zhvi_bdrmcnt_3_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')
zhvi_4bdr = pd.read_csv('Metro_zhvi_bdrmcnt_4_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')
zhvi_5bdr = pd.read_csv('Metro_zhvi_bdrmcnt_5_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')

# Data Transforms
home_pricesT = dt.home_price_transform(home_prices)
inventoryT = dt.home_price_transform(inventory)
list_sale_priceT = dt.home_price_transform(list_sale_price)
mean_days_to_pendingT = dt.home_price_transform(mean_days_to_pending)
price_cutsT = dt.home_price_transform(price_cuts)
percent_below_listT = dt.home_price_transform(percent_below_list)
rentT = dt.home_rent_transform(rent)

zhvi_sfhT = dt.home_price_transform(zhvi_sfh)
zhvi_condosT = dt.home_price_transform(zhvi_condos)
zhvi_1bdrT = dt.home_price_transform(zhvi_1bdr)
zhvi_2bdrT = dt.home_price_transform(zhvi_2bdr)
zhvi_3bdrT = dt.home_price_transform(zhvi_3bdr)
zhvi_4bdrT = dt.home_price_transform(zhvi_4bdr)
zhvi_5bdrT = dt.home_price_transform(zhvi_5bdr)

num_beds = {
    'All Single Family Homes' : zhvi_sfhT,
    'Condos' : zhvi_condosT,
    '1 Bedroom' : zhvi_1bdrT,
    '2 Bedrooms' : zhvi_2bdrT,
    '3 Bedrooms' : zhvi_4bdrT,
    '4 Bedrooms' : zhvi_5bdrT 
}

# App ----------------------
theme_choice = 'FLATLY'
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[getattr(dbc.themes, theme_choice), dbc_css])
app.layout = dbc.Container(
    [
        html.P(style={'margin': 10}),
        html.H1('Housing Market Trends', style={'textAlign': 'center', 'font-weight': 'bold'}),
        html.H3('Home Prices', className="bg-primary text-light"),
        dbc.Row(dcc.Dropdown(home_pricesT.columns, 
                    id='city_selection', 
                    value= home_pricesT.columns[1:6], # Initial placeholder
                    multi=True, 
                    placeholder="Select a city",
                    className="dbc"
                    )
        ),
        html.Div(id='city_output_container'),
        dbc.Row(dcc.Graph(id='home_prices_graph')), # Home Value Graph
        html.H3('Home Prices based on Home Type', className="bg-primary text-light"),
        dbc.Row(dcc.Dropdown(list(num_beds), 
                    id='bed_selection', 
                    value= 'All Single Family Homes',
                    multi=False, 
                    placeholder="Select the type of Home",
                    className="dbc"
                    )
        ),
        dbc.Row(dcc.Graph(id='bedroom_prices_graph')), # Home Value Graph based on number of bedrooms
        html.H3('Inventory', className="bg-primary text-light"),
        dbc.Row(dcc.Graph(id='inventory_graph')), # Inventory Graph
        html.H3('Sale Price', className="bg-primary text-light"),
        dbc.Row(dcc.Graph(id='list_price_graph')), # Sale Price Graph
        html.H3('Sale to List Ratio', className="bg-primary text-light"),
        dbc.Row(dcc.Graph(id='mean_days_to_pending_graph')), # List to Sale Graph
        html.H3('Price Cut', className="bg-primary text-light"),
        dbc.Row(dcc.Graph(id='price_cut_graph')), # Price Cut Graph
        html.H3('Percent of Homes that Sold Below List Price', className="bg-primary text-light"),
        dbc.Row(dcc.Graph(id='percent_below_list_graph')), # Percent below list
        html.H3('Rent', className="bg-primary text-light"),
        dbc.Row(dcc.Graph(id='rent_graph')), # Rental Rates Graph
        html.H6([
            "Made possible thanks to Zillow's public data @ ",
            html.A("https://www.zillow.com/research/data/", href='https://www.zillow.com/research/data/')
        ]),  
    ],
    fluid=True,
    className="dbc"
)
# Callback for Home Value Estimate
@app.callback(
    Output(component_id='home_prices_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(city_selection):
    home_selection = home_pricesT[city_selection] # New dataframe with only columns from selection
    # Makes the Bootstrap Themed Plotly templates available
    load_figure_template(theme_choice)
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Zillow Home Value Index - i.e. the typical home value for each region',
                   xaxis_title='Date',
                   yaxis_title='Home Value ($)',
                   height=600,
                   template=theme_choice)
    return fig

# Callback for Home Value Estimate based on Bedrooms
@app.callback(
    Output(component_id='bedroom_prices_graph', component_property='figure'), # Output graph
    Input(component_id='bed_selection', component_property='value'),
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(bed_selection, city_selection):
    home_type = num_beds[bed_selection]
    home_selection = home_type[city_selection] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Zillow Home Value Index for the Type of Home Selected',
                   xaxis_title='Date',
                   yaxis_title='Home Value ($)',
                   height=600,
                   template=theme_choice)
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
                   height=600,
                   template=theme_choice)
    return fig

# Callback for Sale Price
@app.callback(
    Output(component_id='list_price_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = list_sale_priceT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Median Sale Price (All homes, monthly)',
                   xaxis_title='Date',
                   yaxis_title='Price ($)',
                   height=600,
                   template=theme_choice)
    return fig

# Callback for List to Sale
@app.callback(
    Output(component_id='mean_days_to_pending_graph', component_property='figure'), # Output graph
    Input(component_id='city_selection', component_property='value') # Input dropdown city selections
)
def update_graph(cities):
    home_selection = mean_days_to_pendingT[cities] # New dataframe with only columns from selection
    fig = px.line(home_selection, x=home_selection.index, y=home_selection.columns) # Graph with new dataframe
    fig.update_layout(title='Mean Days to Pending Sale',
                   xaxis_title='Date',
                   yaxis_title='Days',
                   height=600,
                   template=theme_choice)
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
                   height=600,
                   template=theme_choice)
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
                   height=600,
                   template=theme_choice)
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
                   height=600,
                   template=theme_choice)
    return fig 

if __name__ == '__main__':
    app.run_server(debug=True)