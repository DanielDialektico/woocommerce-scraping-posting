from typing import Protocol, List
import pandas as pd

class URLsFactoryServiceProtocol(Protocol):
    def __init__(self) -> None:
        ...

    def extract_filter_path(self) -> str:
        ...

    def filter_urls(self, urls: List[str]) -> pd.DataFrame:
        ...

    def save_urls_csv(self, df: pd.DataFrame) -> None:
        ...