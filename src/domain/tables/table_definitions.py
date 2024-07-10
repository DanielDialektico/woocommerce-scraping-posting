import pandas as pd
from typing import List
from src.config.config import WOOC_SAMPLE
from src.common.utils import files_output_path
from src.domain.abstractions import TableDefinitionsProtocol

class TableDefinitions(TableDefinitionsProtocol):
    """
    Implementation of the TableDefinitionsProtocol to provide methods
    for creating product and URL tables as pandas DataFrames.
    """

    @staticmethod
    def product_table() -> pd.DataFrame:
        """
        Create an empty product table DataFrame with the same columns
        as a sample CSV file.

        Returns:
            pd.DataFrame: An empty DataFrame with columns matching the sample CSV.
        """
        # Define the path to the sample CSV file.
        sample_csv_path = files_output_path('files\\tables', WOOC_SAMPLE)
        
        # Read the sample CSV file to get column definitions.
        sample_df = pd.read_csv(sample_csv_path, encoding='utf-8')
        
        # Create an empty DataFrame with the same columns as the sample CSV.
        product_df = pd.DataFrame(columns=sample_df.columns)
        
        return product_df

    @staticmethod
    def urls_table(urls: List[str]) -> pd.DataFrame:
        """
        Create a DataFrame containing a single column 'URL' populated
        with the given list of URLs.

        Args:
            urls (List[str]): A list of URLs to include in the DataFrame.

        Returns:
            pd.DataFrame: A DataFrame with a single 'URL' column.
        """
        # Create a DataFrame from the list of URLs.
        urls_df = pd.DataFrame(urls, columns=['URL'])
        
        return urls_df