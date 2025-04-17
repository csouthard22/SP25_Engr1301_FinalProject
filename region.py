import util
import pandas as pd
import json
import matplotlib.pyplot as plt

class Region:
    def __init__(self, name):
        """
        Initialize a Region object.

        Args:
            name (str): The name of the region (e.g., state name or 'US').
        """
        self.name = util.name_resolver(name)
        self.data = {}


    def _grab_data(self,start_year,end_year=None):
        """
        Grabs all data for the region, given a range of years.

        Args:
            start_year (int): Starting year for data collection
            end_year (int): Ending year for data collection
        Returns:
            None. Updates self.data dictionary
        """
        fileList = util.tri_file_pointer(start_year,end_year)

        if self.name == 'US':
            for file in fileList:
                df = pd.read_csv(file,true_values=['YES'],false_values=['NO'])
                year = file.split('/')[-1].split('_')[0]
                self.data[year] = df
        else:
            for file in fileList:
                df = pd.read_csv(file,true_values=['YES'],false_values=['NO'])
                df_filtered = df[df['ST'] == self.name]
                year = file.split('/')[-1].split('_')[0]
                self.data[year] = df_filtered


    def _get_emissions(self, start_year, end_year=None):
        """
        Calculate the total emissions for the region.

        Returns:
            float: Total emissions.
        """
        pass
        self._grab_data(start_year,end_year)
        total = 0.0

    def top_polluted_cities(self, numCities=5):
        pass

    def top_polluting_industries(self, numIndustries=5):
        pass

    def top_polluting_companies(self, numCompanies=5):
        pass

    def pollution_heatmap(self):
        pass #use pyplot

    def top_chemicals(self, numChemicals=5):
        pass
    
    def how_cancerous(self):
        pass # out of ___ pounds of pollution, ___ pounds (_%) were carcinogens

    def pct_forever_chemicals(self):
        pass

    def emissions_by_year(self,start_year, end_year=None):
        """
        Get emissions data grouped by year.

        Returns:
            pd.DataFrame: Emissions data grouped by year.
        """
        if end_year == None: end_year = start_year
        pass  # Implement logic to group emissions by year


    def top_polluters(self, n=10):
        """
        Get the top N polluters in the region.

        Args:
            n (int): Number of top polluters to return.

        Returns:
            pd.DataFrame: Data of the top N polluters.
        """
        pass  # Implement logic to find top polluters

    def plot_trend(self,start_year=1987,end_year=2023):
        """
        Plot the trend of emissions over time for the region.

        Args:
            start_year (int): Starting year of trend. Default 1987
            end_year (int): Ending year of trend. Default 1987
        """
        pass  # Implement logic to plot emissions trend

    def compare(self, other_region):
        """
        Compare emissions data with another region.

        Args:
            other_region (Region): Another Region object to compare with.

        Returns:
            dict: Comparison metrics between the two regions.
        """
        pass  # Implement logic to compare with another region