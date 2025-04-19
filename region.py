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

    def _total_emissions(self, start_year, end_year=None):
        """
        Calculate the total emissions for the region within the specified year range.

        Args:
            start_year (int): Starting year for data collection
            end_year (int): Ending year for data collection

        Returns:
            float: Total emissions within the specified year range.
        """
        self._grab_data(start_year, end_year)
        total_emissions = 0.0

        if end_year == None: end_year = start_year

        for year, df in self.data.items():
            if int(year) >= start_year and int(year) <= end_year:
                total_emissions += df['TOTAL POLLUTION'].sum()

        return total_emissions

    def top_polluted_cities(self, start_year, end_year=None, numCities=5):
        """
        Identifies the top polluted cities based on total pollution over a specified time range.

        This method processes pollution data for the given range of years, aggregates the total 
        pollution for each city, and returns the top cities with the highest pollution levels.

        Args:
            start_year (int): The starting year of the range for which pollution data is analyzed.
            end_year (int, optional): The ending year of the range for which pollution data is analyzed. Defaults to start year.
            numCities (int, optional): The number of top polluted cities to return. Defaults to 5.

        Returns:
            list: A list of tuples where each tuple contains a city name (str) and its total 
                  pollution (float), sorted in descending order of pollution. The list contains 
                  up to `numCities` entries.
        """
        self._grab_data(start_year,end_year)
        city_emissions = {}

        for year, df in self.data.items():
            cities = df.groupby('CITY')['TOTAL POLLUTION'].sum()
            for city, emissions in cities.items():
                if city in city_emissions:
                    city_emissions[city] += emissions
                else:
                    city_emissions[city] = emissions

        sorted_cities = sorted(city_emissions.items(), key=lambda x: x[1], reverse=True)
        return sorted_cities[:numCities]

    def top_polluting_industries(self, start_year, end_year=None, numIndustries=5):
        """
        Identifies the top polluting industries within a specified time range.

        This method calculates the total pollution emitted by each industry sector
        over the specified range of years and returns the top industries based on
        their total emissions.

        Args:
            start_year (int): The starting year of the range for which data is analyzed.
            end_year (int, optional): The ending year of the range for which data is analyzed. Defaults to start year
            numIndustries (int, optional): The number of top polluting industries to return. Defaults to 5.

        Returns:
            list of tuple: A list of tuples where each tuple contains an industry sector (str)
            and its corresponding total pollution (float), sorted in descending order of pollution.
            The list contains up to `numIndustries` entries.
        """
        self._grab_data(start_year,end_year)
        industry_emissions = {}

        for year, df in self.data.items():
            industries = df.groupby('INDUSTRY SECTOR')['TOTAL POLLUTION'].sum()
            for industry, emissions in industries.items():
                if industry in industry_emissions:
                    industry_emissions[industry] += emissions
                else:
                    industry_emissions[industry] = emissions

        sorted_industries = sorted(industry_emissions.items(), key=lambda x: x[1], reverse=True)
        return sorted_industries[:numIndustries]

    def pollution_heatmap(self):
        pass #use pyplot

    def top_chemicals(self, start_year, end_year=None, numChemicals=5):
        """
        Identify the top chemicals contributing to pollution over a specified time range.

        This method calculates the total pollution caused by each chemical across the 
        specified years and returns the top `numChemicals` chemicals with the highest 
        pollution levels.

        Args:
            start_year (int): The starting year for the data analysis.
            end_year (int, optional): The ending year for the data analysis. Defaults to start year
            numChemicals (int, optional): The number of top chemicals to return. Defaults to 5.

        Returns:
            list of tuple: A list of tuples where each tuple contains a chemical name 
            (str) and its total pollution (float), sorted in descending order of 
            pollution. The length of the list is determined by `numChemicals`.
        """
        self._grab_data(start_year,end_year)
        chemicals_list = {}

        for year, df in self.data.items():
            chemicals = df.groupby('CHEMICAL')['TOTAL POLLUTION'].sum()
            for chemical, emissions in chemicals.items():
                if chemical in chemicals_list:
                    chemicals_list[chemical] += emissions
                else:
                    chemicals_list[chemical] = emissions

        sorted_chemicals = sorted(chemicals_list.items(), key=lambda x: x[1], reverse=True)
        return sorted_chemicals[:numChemicals]
    
    def how_cancerous(self):
        pass # out of ___ pounds of pollution, ___ pounds (_%) were carcinogens

    def pct_forever_chemicals(self):
        pass

    def emissions_by_year(self,start_year, end_year):
        """
        Get emissions data grouped by year.

        Returns:
            pd.DataFrame: Emissions data grouped by year.
        """
        pass  # Implement logic to group emissions by year

    def top_polluters(self, n=5):
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