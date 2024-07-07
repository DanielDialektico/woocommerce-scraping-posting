from typing import Protocol
import pandas as pd

class DataPreparationServiceProtocol(Protocol):
    """
    Protocol defining the methods for data preparation services.
    """

    def _convert_attributes(self, row: pd.Series) -> pd.Series:
        ...

    def prepare_data(self, csv_name: str) -> pd.DataFrame:
        ...

    def process_images(self, image_urls: str) -> list:
        ...
