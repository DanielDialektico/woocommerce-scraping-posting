from urllib.parse import urlparse
import pandas as pd
from src.domain.tables import TableDefinitions
from src.common.utils import files_output_path
from src.config.config import PRODUCT_URLS_CSV, CATEGORIES_URL
from src.domain.abstractions import URLsFactoryServiceProtocol

class URLsFactoryService(URLsFactoryServiceProtocol):
    """
    A service class for filtering URLs in a DataFrame.
    """

    def __init__(self):
        """
        Initializes the URLsFactoryService.

        Expected input:
        - None

        Expected output:
        - None (initializes self.categories_url and self.table_creator)
        """
        self.categories_url = CATEGORIES_URL
        self.table_creator = TableDefinitions

    def extract_filter_path(self) -> str:
        """
        Extract the path from the categories URL to use as a filter criterion.

        Expected input:
        - None

        Expected output:
        - str: The path segment to filter URLs.
        """
        parsed_url = urlparse(self.categories_url)
        return parsed_url.path.rstrip('/')

    def filter_urls(self, urls: list) -> pd.DataFrame:
        """
        Filter the list of URLs and return a DataFrame with unique cleaned URLs.

        Expected input:
        - urls (list): List of URLs to filter.

        Expected output:
        - pd.DataFrame: DataFrame with filtered and cleaned URLs.
        """
        filter_path = self.extract_filter_path()

        df = self.table_creator.urls_table(urls)

        # Filter URLs that contain the specific categories path
        df_filtered = df[df['URL'].str.contains(filter_path, case=False)].copy()

        # Clean the full URL by removing everything after the question mark
        df_filtered.loc[:, 'Cleaned_URL'] = df_filtered['URL'].apply(lambda url: url.split('?')[0])

        # Remove duplicates
        df_unique = df_filtered.drop_duplicates(subset='Cleaned_URL')

        return df_unique
    
    def save_urls_csv(self, df: pd.DataFrame):
        """
        Save the filtered DataFrame to a CSV file.

        Expected input:
        - df (pd.DataFrame): DataFrame with filtered URLs.

        Expected output:
        - None (saves the DataFrame to a CSV file and prints the number of saved URLs)
        """
        output_path = files_output_path('files\\tables', PRODUCT_URLS_CSV)
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f'{len(df)} URLs have been saved to {output_path}')