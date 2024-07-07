from typing import Protocol, List
import pandas as pd

class TableDefinitionsProtocol(Protocol):
    """
    Protocol defining the methods for table definition operations.
    Classes implementing this protocol should provide methods for
    creating product and URL tables as pandas DataFrames.
    """

    def product_table(self) -> pd.DataFrame:
        """
        Create an empty product table DataFrame.

        Returns:
            pd.DataFrame: An empty DataFrame with columns predefined.
        """
        ...

    def urls_table(self, urls: List[str]) -> pd.DataFrame:
        """
        Create a DataFrame containing a single column 'URL' populated
        with the given list of URLs.

        Args:
            urls (List[str]): A list of URLs to include in the DataFrame.

        Returns:
            pd.DataFrame: A DataFrame with a single 'URL' column.
        """
        ...
