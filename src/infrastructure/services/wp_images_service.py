import os
import requests
from urllib.parse import urljoin
from src.config.config import WP_URL, WP_USERNAME, WP_PASSWORD
from src.domain.abstractions import WPImagesServiceProtocol

class WPImagesService(WPImagesServiceProtocol):
    """
    A service class for uploading images to a WordPress site.
    """

    def upload_image(self, image_path: str) -> str:
        """
        Upload an image to WordPress.

        Args:
            image_path (str): The path to the image file to be uploaded.

        Returns:
            str: The URL of the uploaded image.

        Raises:
            requests.exceptions.RequestException: An error occurred while making the HTTP request.
            KeyError: The response does not contain the expected 'source_url'.
        """
        try:
            with open(image_path, 'rb') as img:
                media = {
                    'file': img,
                    'caption': 'Uploaded using API',
                    'description': 'Uploaded using API'
                }
                headers = {
                    'Content-Disposition': f'attachment; filename={os.path.basename(image_path)}'
                }
                response = requests.post(
                    urljoin(WP_URL, 'media'),
                    headers=headers,
                    files=media,
                    auth=(WP_USERNAME, WP_PASSWORD)
                )
                response.raise_for_status()
                return response.json()['source_url']
        except requests.exceptions.RequestException as e:
            print(f"HTTP error occurred: {e}")
        except KeyError as e:
            print(f"Key error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")