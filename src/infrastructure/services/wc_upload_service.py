from woocommerce import API
from src.config.config import WC_URL, WC_KEY, WC_SECRET, WC_VERSION, WC_TIMEOUT
import requests
from src.domain.abstractions import WCUploadServiceProtocol

class WCUploadService(WCUploadServiceProtocol):
    """
    A service class for uploading products and variations to WooCommerce.
    """

    def __init__(self):
        """
        Initialize the WooCommerce API client with the provided configuration.
        """
        self.wcapi = API(
            url=WC_URL,
            consumer_key=WC_KEY,
            consumer_secret=WC_SECRET,
            version=WC_VERSION,
            timeout=WC_TIMEOUT
        )

    def create_product(self, product_data):
        """
        Create a product in WooCommerce.

        Args:
            product_data (dict): The data for the product to be created.

        Returns:
            Response: The response from the WooCommerce API.
        """
        try:
            # Convert the price to string
            product_data['regular_price'] = str(product_data.get('regular_price', ''))
            
            # Remove unnecessary parameters for simple and variable products
            product_data.pop('download_limit', None)
            product_data.pop('download_expiry', None)
            
            # Send a POST request to create the product
            response = self.wcapi.post("products", data=product_data)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            print(f"An error occurred: {err}")
            return None

    def create_variation(self, product_id, variation_data):
        """
        Create a product variation in WooCommerce.

        Args:
            product_id (int): The ID of the product to add the variation to.
            variation_data (dict): The data for the variation to be created.

        Returns:
            Response: The response from the WooCommerce API.
        """
        try:
            # Convert the price to string
            variation_data['regular_price'] = str(variation_data.get('regular_price', ''))
            
            # Send a POST request to create the variation
            response = self.wcapi.post(f"products/{product_id}/variations", data=variation_data)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            print(f"An error occurred: {err}")
            return None