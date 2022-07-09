# An app that displays the latest housing data from Zillow

# Imports
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
home_prices = dt.home_price_transform() # Zillow Home Value Index 
# inventory         =>  Home Inventory 
# list_sale_price   => List and Sale Prices
# price_cuts        => Sales Count and Price Cuts

# Graphs

fig = px.line(dt.home_prices, x=houseT.index, y=houseT['Los Angeles-Long Beach-Anaheim, CA'])
fig.show()