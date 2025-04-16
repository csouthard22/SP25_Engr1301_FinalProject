import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import os

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

    if start_year < 1987 or end_year > 2023: return 'ERROR: PLEASE CHOOSE DATA RANGE WITHIN 1987-2023'
    elif end_year<start_year: return 'ERROR: END YEAR IS BEFORE START YEAR'
    else:
        dataFiles += [f'data/tri/{year}_us.csv' for year in range(start_year, end_year+1)]
        return dataFiles
    
