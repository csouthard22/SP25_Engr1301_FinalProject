import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import os
import json

us_states = gpd.read_file('data/us-states.json')
TRI_DATA_DIR = 'data/tri'

def tri_file_pointer(start_year, end_year=None):
    """
    Takes a start year and end year, and returns a list of file names of data from this range.
    Args:
        start_year (int): Beginning year of range.
        end_year (int): Ending year of range. If none given, only returns one year.
    Returns:
        List of file data paths as strings.
        If data outside range, returns error
    """

    if end_year == None: end_year=start_year

    dataFiles = []

    if start_year < 1987 or end_year > 2023: raise ValueError('Please choose data within range 1987-2023')
    elif end_year<start_year: raise ValueError('End year is before start year')
    else:
        dataFiles += [f'data/tri/{year}_us.csv' for year in range(start_year, end_year+1)]
        return dataFiles
    
def name_resolver(name):
    """
    Takes state name as an input. If input is not a state name or 'US', return error. If input is the long-form state name, turn it into the short form.

    Args:
        state (str): Name of state or 'US'
    Returns:
        state name in short form if not already
    """
    with open('data/states-short.json', 'r') as f:
        state_data = json.load(f)

    if name.title() in state_data:
        return state_data[name.title()]

    if name.upper() in state_data.values():
        return name.upper()
    
    raise ValueError(f"'{name}' is not a valid state name or abbreviation.")