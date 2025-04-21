import util
import pandas as pd
import geopandas as gpd
import numpy as np
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

        if end_year is None: end_year = start_year

        for file in fileList:
            year = int(file.split('/')[-1].split('_')[0])
            if start_year <= year <= end_year:
                if year not in self.data:
                    df = pd.read_csv(file, true_values=['YES'], false_values=['NO'])
                    if self.name != 'US':
                        df = df[df['ST'] == self.name]
                    self.data[year] = df

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
        if end_year == None: end_year = start_year

        combined_data = pd.concat(
            [df for year, df in self.data.items() if start_year <= int(year) <= end_year],
            ignore_index=True
        )
        return combined_data['TOTAL POLLUTION'].sum()

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
        return [(city, f"{emissions:.2f} pounds") for city, emissions in sorted_cities[:numCities]]

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
        return [(industry, f"{emissions:.2f} pounds") for industry, emissions in sorted_industries[:numIndustries]]

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
        return [(chemical, f"{emissions:.2f} pounds") for chemical, emissions in sorted_chemicals[:numChemicals]]
    
    def how_cancerous(self, start_year, end_year=None):
        """
        Calculate the proportion of carcinogenic emissions within the specified year range.

        Args:
            start_year (int): Starting year for data collection.
            end_year (int, optional): Ending year for data collection. Defaults to start year.

        Returns:
            str: A summary of the total pollution and the proportion that is carcinogenic.
        """
        total_emissions = self._total_emissions(start_year,end_year)
        self._grab_data(start_year, end_year)
        carcinogenic_emissions = 0.0

        for year, df in self.data.items():
            carcinogenic_emissions += df[df['CARCINOGEN'] == True]['TOTAL POLLUTION'].sum()

        percentage_carcinogenic = (carcinogenic_emissions / total_emissions) * 100

        if end_year == None:
            return f"Out of {total_emissions:.2f} pounds of pollution in {start_year}, {carcinogenic_emissions:.2f} pounds ({percentage_carcinogenic:.2f}%) were carcinogenic."
        else:
            return f"Out of {total_emissions:.2f} pounds of pollution in {start_year}-{end_year}, {carcinogenic_emissions:.2f} pounds ({percentage_carcinogenic:.2f}%) were carcinogenic."

    def pct_forever_chemicals(self, start_year, end_year=None):
        """
        Calculate the percentage of pollution attributed to PFAS (forever chemicals) 
        within a specified time range.

        Args:
            start_year (int): The starting year for the calculation.
            end_year (int, optional): The ending year for the calculation. Defaults to None.

        Returns:
            str: A formatted string indicating the total pollution, the amount of 
                 pollution attributed to PFAS, and the percentage of PFAS pollution 
                 for the specified time range.
        """
        total_emissions = self._total_emissions(start_year,end_year)
        self._grab_data(start_year, end_year)
        pfa_emissions = 0.0

        for year, df in self.data.items():
            pfa_emissions += df[df['PFAS'] == True]['TOTAL POLLUTION'].sum()

        percentage_pfa = (pfa_emissions / total_emissions) * 100


        if end_year == None:
            return f"Out of {total_emissions:.2f} pounds of pollution in {start_year}, {pfa_emissions:.2f} pounds ({percentage_pfa:.2f}%) were PFAs (forever chemicals)."
        else:
            return f"Out of {total_emissions:.2f} pounds of pollution in {start_year}-{end_year}, {pfa_emissions:.2f} pounds ({percentage_pfa:.2f}%) were PFAs (forever chemicals)."

    def top_polluting_companies(self, start_year, end_year=None, numCompanies=5):
        """
        Identifies the top polluting companies within a specified time range.

        This method calculates the total pollution emitted by each company 
        across the specified years and returns the top `numCompanies` 
        contributors to pollution.

        Args:
            start_year (int): The starting year for the data analysis.
            end_year (int, optional): The ending year for the data analysis. Defaults to start year.
            numCompanies (int, optional): The number of top polluting companies 
                to return. Defaults to 5.

        Returns:
            list: A list of tuples, where each tuple contains a company name 
            (str) and its total pollution (float), sorted in descending order 
            of pollution. The length of the list is determined by `numCompanies`.
        """
        self._grab_data(start_year)
        companies_list = {}

        for year, df in self.data.items():
            companies = df.groupby('PARENT CO NAME')['TOTAL POLLUTION'].sum()
            for company, emissions in companies.items():
                if company in companies_list:
                    companies_list[company] += emissions
                else:
                    companies_list[company] = emissions

        sorted_companies = sorted(companies_list.items(), key=lambda x: x[1], reverse=True)
        return [(company, f"{emissions:.2f} pounds") for company, emissions in sorted_companies[:numCompanies]]

    def pollution_heatmap(self, start_year, end_year=None):
        states_gdf = util.us_states
        self._grab_data(start_year, end_year)

        if end_year is None:
            end_year = start_year

        combined_data = pd.DataFrame()
        for year, df in self.data.items():
            combined_data = pd.concat([combined_data, df])

        pollution_gdf = gpd.GeoDataFrame(
            combined_data,
            geometry=gpd.points_from_xy(combined_data['LONGITUDE'], combined_data['LATITUDE'])
        )

        if self.name == 'US':
            ax = states_gdf.plot(color='white', edgecolor='black', figsize=(15, 10))
        else:
            state_gdf = states_gdf[states_gdf['NAME'] == self.name]
            ax = state_gdf.plot(color='white', edgecolor='black', figsize=(15, 10))
        """ ^^^^^^^^^^^^^^^^^^^^
        fix later. need to make it so that i can match the name in the json (long form) to self.name (abbreviation)
        maybe can do this with some sort of backwards util.name_resolver
        also the state_gdf = ... is not correct notation for a json but ill leave it there so i keep the essence of what im trying to do
        too tired to keep working. goodnight
        """
        pollution_gdf.plot(
            ax=ax,
            markersize=pollution_gdf['TOTAL POLLUTION'] / pollution_gdf['TOTAL POLLUTION'].max() * 100,
            color='red',
            alpha=0.5
        )

        plt.title(f"Pollution Heatmap ({start_year}-{end_year}) - {self.name}", fontsize=16)
        plt.xlabel("Longitude", fontsize=12)
        plt.ylabel("Latitude", fontsize=12)
        plt.show()

    def plot_trend(self,start_year=1987,end_year=2023):
        def plot_trend(self, start_year=1987, end_year=2023):
            """
            Plots the pollution trend for the region over a specified range of years.

            This method generates a line plot comparing the total emissions of the region
            to the average emissions of the United States over the specified time period.
            The emissions are displayed in billions of pounds.

            Args:
                start_year (int, optional): The starting year for the trend plot. Defaults to 1987.
                end_year (int, optional): The ending year for the trend plot. Defaults to 2023.

            Returns:
                - None. Displays a matplotlib plot showing the emissions trend for the region and the US average.
            """
        years = np.arange(start_year, end_year + 1)
        emissions = np.array([self._total_emissions(year) for year in years]) / 1000000000
        us_emissions = np.array([Region('US')._total_emissions(year) for year in years]) / 50 / 1000000000

        plt.plot(years,emissions, label=f"{self.name} Emissions", color='blue')
        plt.plot(years,us_emissions, label="US Average Emissions (per state)", color='orange', linestyle='--')
        plt.title(f"{self.name} Pollution Trend ({start_year}-{end_year})", fontsize=16)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Total Emissions (Billion Pounds)", fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.show
        

    def compare(self, other_region):
        """
        Compare emissions data with another region.

        Args:
            other_region (Region): Another Region object to compare with.

        Returns:
            dict: Comparison metrics between the two regions.
        """
        pass  # Implement logic to compare with another region