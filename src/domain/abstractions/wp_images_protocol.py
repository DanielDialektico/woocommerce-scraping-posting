from typing import Protocol

class WPImagesServiceProtocol(Protocol):
    def upload_image(self, image_path: str) -> str:
        ...