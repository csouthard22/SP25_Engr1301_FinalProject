import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import os

us_states = gpd.read_file('data/us-states.json')
TRI_DATA_DIR = 'data/tri'

print("Executing util.py")
print("Loaded US states GeoDataFrame:")
print(us_states.head())
print("TRI data directory:", TRI_DATA_DIR)