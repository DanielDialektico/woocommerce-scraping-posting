from typing import Protocol, List
import pandas as pd

class TablesFactoryServiceProtocol(Protocol):
    def __init__(self) -> None:
        ...

    def _create_variant_df(self, variant, title: str, brand: str, tags: List[str], parent_sku: str, image_name: str, attribute_name: str) -> pd.DataFrame:
        ...

    def _create_parent_df(self, title: str, sku: str, price: float, description: str, brand: str, tags: List[str], attribute_name: str, attribute_values: List[str], gallery_images: List[str]) -> pd.DataFrame:
        ...

    def _create_simple_df(self, title: str, sku: str, price: float, description: str, brand: str, tags: List[str], image_name: str, gallery_images: List[str]) -> pd.DataFrame:
        ...

    def create_tables(self, product_data: dict, title: str, price: float, description: str, brand: str, tags: List[str], image_names: List[str], attribute_name: str) -> pd.DataFrame:
        ...

    def save_products_csv(self, df: pd.DataFrame) -> None:
        ...
