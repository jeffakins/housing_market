# A file to store functions that transform the Zillow data

# Imports
import pandas as pd

# Functions
def home_price_transform(house):
    '''Transforms the the Zillow Home Value Index dataframe into a format
    that can be used for a timeseries line graph in plotly'''
    house = house.drop(columns=['RegionID', 'SizeRank', 'RegionType', 'StateName'])
    house = house.set_index('RegionName')
    house = house.T
    return house
