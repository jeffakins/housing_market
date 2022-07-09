# A file to store functions that transform the Zillow data

# Imports
import pandas as pd

# Data
home_prices = pd.read_csv('Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv') # Zillow Home Value Index 
inventory = pd.read_csv('Metro_invt_fs_uc_sfrcondo_sm_month.csv') # Home Inventory 
list_sale_price = pd.read_csv('Metro_mlp_uc_sfrcondo_sm_month.csv') # List and Sale Prices
price_cuts = pd.read_csv('Metro_sales_count_now_uc_sfrcondo_month.csv') # Sales Count and Price Cuts

# Functions
def home_price_transform(home_prices):
    '''Transforms the the Zillow Home Value Index dataframe into a format
    that can be used for a timeseries line graph in plotly'''
    house = house.drop(columns=['RegionID', 'SizeRank', 'RegionType', 'StateName'])
    house = house.set_index('RegionName')
    house = house.T
    return house