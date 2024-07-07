from typing import Protocol

class ImagesUploadPipelineProtocol(Protocol):
    def __init__(self, container) -> None:
        ...

    def run(self) -> None:
        ...