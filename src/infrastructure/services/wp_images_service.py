import os
import requests
from urllib.parse import urljoin
from src.config.config import WP_URL, WP_USERNAME, WP_PASSWORD
from src.domain.abstractions import WPImagesServiceProtocol
import time

class WPImagesService(WPImagesServiceProtocol):
    """
    A service class for uploading images to a WordPress site.
    """

    def upload_image(self, image_path: str, retries=3, wait_time=2) -> str:
        """
        Upload an image to WordPress.

        Args:
            image_path (str): The path to the image file to be uploaded.
            retries (int): Number of times to retry the upload in case of failure.
            wait_time (int): Number of seconds to wait between retries.

        Returns:
            str: The URL of the uploaded image.

        Raises:
            requests.exceptions.RequestException: An error occurred while making the HTTP request.
            KeyError: The response does not contain the expected 'source_url'.
        """
        attempt = 0
        while attempt < retries:
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
                        auth=(WP_USERNAME, WP_PASSWORD),
                        timeout=10  # Timeout for the request
                    )
                    response.raise_for_status()
                    return response.json()['source_url']
            except requests.exceptions.RequestException as e:
                print(f"HTTP error occurred: {e}")
                attempt += 1
                if attempt < retries:
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            except KeyError as e:
                print(f"Key error occurred: {e}")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        print(f"Failed to upload image {image_path} after {retries} attempts.")