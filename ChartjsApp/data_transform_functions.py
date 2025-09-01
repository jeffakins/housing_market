# A file to store functions that transform the Zillow data

# Imports
import pandas as pd

# Functions
def home_price_transform(house_csv):
    '''Transforms the the Zillow Home Value Index dataframe into a format
    that can be used for a timeseries line graph in json format for chartjs'''
    house = pd.read_csv(house_csv)
    house = house.drop(columns=['RegionID', 'SizeRank', 'RegionType', 'StateName'])
    house = house.set_index('RegionName').sort_index()
    house = house.T
    return house

def home_rent_transform(house):
    '''Transforms the the Zillow Home Rental Rate dataframe into a format
    that can be used for a timeseries line graph in plotly'''
    house = house.drop(columns=['RegionID', 'SizeRank'])
    house = house.set_index('RegionName')
    house = house.T
    return house