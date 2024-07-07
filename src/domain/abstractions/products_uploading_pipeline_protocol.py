from typing import Protocol

class ProductsUploadingPipelineProtocol(Protocol):
    def __init__(self, container):
        ...

    def run(self):
        ...