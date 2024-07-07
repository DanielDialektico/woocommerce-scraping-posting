from typing import Protocol, Dict

class WCUploadServiceProtocol(Protocol):
    def __init__(self) -> None:
        ...

    def create_product(self, product_data: Dict) -> Dict:
        ...

    def create_variation(self, product_id: int, variation_data: Dict) -> Dict:
        ...