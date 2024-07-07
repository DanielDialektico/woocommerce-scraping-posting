from typing import Protocol, Any, List, Dict

class WebsiteScrapingPipelineProtocol(Protocol):
    def __init__(self, container: Any) -> None:
        ...

    def run(self) -> None:
        ...