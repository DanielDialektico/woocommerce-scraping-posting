from typing import Protocol, List

class BSCrawlingWebServiceProtocol(Protocol):
    def __init__(self) -> None:
        ...

    def url_validator(self, url: str, domain: str, prefix: str) -> bool:
        ...

    def crawling_web(self) -> List[str]:
        ...

    def update_prefix(self) -> None:
        ...