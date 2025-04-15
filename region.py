
class Region:
    def __init__(self, name, data):
        """
        Initialize a Region object.

        Args:
            name (str): The name of the region (e.g., state name or 'US').
            data (pd.DataFrame): The data associated with the region.
        """
        self.name = name
        self.data = data

    def get_total_emissions(self):
        """
        Calculate the total emissions for the region.

        Returns:
            float: Total emissions.
        """
        pass  # Implement logic to calculate total emissions

    def emissions_by_year(self):
        """
        Get emissions data grouped by year.

        Returns:
            pd.DataFrame: Emissions data grouped by year.
        """
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