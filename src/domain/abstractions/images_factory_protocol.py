from typing import Protocol, List
import pandas as pd

class ImagesFactoryServiceProtocol(Protocol):
    def __init__(self) -> None:
        ...
    
    def create_paths_table(self) -> pd.DataFrame:
        ...
    
    def update_wc_table(self, paths_df: pd.DataFrame, image_urls: List[str]) -> pd.DataFrame:
        ...
    
    def save_updated_csv(self, df: pd.DataFrame) -> None:
        ...