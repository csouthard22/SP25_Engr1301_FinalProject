import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import os

us_states = gpd.read_file('data/us-states.json')

# Define the rows to delete (1-based index)
rows_to_delete = [1, 2, 3, 5, 7, 9, 10, 11, 14] + list(range(16, 21)) + [22] + list(range(24, 37)) + [39, 40, 41, 44, 45]
rows_to_delete = [r - 1 for r in rows_to_delete]  # Convert to 0-based index

# Directory containing the CSV files
tri_raw_dir = 'data/tri_raw'

# Iterate through all CSV files in the directory
for filename in os.listdir(tri_raw_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(tri_raw_dir, filename)

        # Read the CSV file
        df = pd.read_csv(file_path, low_memory=False)

        # Drop the specified rows
        df = df.drop(rows_to_delete, errors='ignore')

        # Save the updated DataFrame back to the same file
        df.to_csv(file_path, index=False)