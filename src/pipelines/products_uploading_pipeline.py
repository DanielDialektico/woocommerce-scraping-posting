import os
from src.common.utils import setup_logging
from src.config.config import LOGGING_PRODUCTS_FILE, UPDATED_PRODUCTS_CSV, WC_URL
from src.domain.abstractions import ProductsUploadingPipelineProtocol

# Initialize logger
logger = setup_logging(LOGGING_PRODUCTS_FILE)

class ProductsUploadingPipeline(ProductsUploadingPipelineProtocol):
    """
    A pipeline class for uploading products to WooCommerce.
    """

    def __init__(self, container):
        """
        Initialize the ProductsUploadingPipeline with the given container.

        Args:
            container (object): The dependency injection container.
        """
        self.container = container
        self.data_preparation_service = container.config('data_preparation_service')
        self.wc_upload_service = container.config('wc_upload_service')
        self.images_column = 'image_id/gallery_image_ids'

    def run(self):
        """
        Run the product upload pipeline.
        """
        print("\n-----Wordpress Products Creating Stage-----\n")
        logger.info("Starting Wordpress Products Uploading Stage")

        print("Preparing data...")
        logger.info("Preparing data...")
        products = self.prepare_data()
        if not products:
            return

        parent_id_map = {}
        self.create_variable_products(products, parent_id_map)
        self.create_variations(products, parent_id_map)
        self.create_simple_products(products)

        total_created = len(parent_id_map) + len([p for p in products if p['type'] == 'simple']) + len([p for p in products if p['type'] == 'variation'])
        print(f"\n{total_created} products have been created in {WC_URL}.")
        logger.info(f'{total_created} products have been created in {WC_URL}.')

    def prepare_data(self):
        """
        Prepare data for uploading.
        """
        try:
            products = self.data_preparation_service.prepare_data(UPDATED_PRODUCTS_CSV)
            print('Data prepared.')
            logger.info('Data prepared.')
            return products
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return None

    def create_variable_products(self, products, parent_id_map):
        """
        Create variable products and their default variants.
        """
        print("\nCreating variable products...")
        logger.info("Creating variable products...")    

        counter_v = 0
        for product in products:
            if product['type'] == 'variable':
                self.create_variable_product(product, parent_id_map)
                counter_v += 1
                if counter_v % 50 == 0:
                    print(f'\n{counter_v} variable products created.')
                    logger.info(f'\n{counter_v} variable products created.')

    def create_variable_product(self, product, parent_id_map):
        """
        Create a single variable product and its default variants.
        """
        try:
            product['sku'] = product['sku'] + 'v'
            product.pop('parent_id', None)
            product['images'] = self.data_preparation_service.process_images(product.get(self.images_column, ''))
            product['attributes'] = product.get('attributes', [])
            product['default_attributes'] = product.get('default_attributes', [])
            response = self.wc_upload_service.create_product(product)
            if response.status_code == 201:
                product_id = response.json()['id']
                parent_id_map[product['sku']] = product_id
                logger.info(f"Variable product '{product['name']}' created successfully with ID {product_id}.")
                self.create_default_variants(product, product_id)
            else:
                logger.info(f"Error creating product '{product['name']}']: {response.json()}")
        except Exception as e:
            logger.error(f"Error creating variable product '{product['name']}': {e}")

    def create_default_variants(self, product, product_id):
        """
        Create default variants for a variable product.
        """
        for default_attr in product['default_attributes']:
            variation_data = {
                "sku": product['sku'][:-1],
                "regular_price": product['regular_price'],
                "image": {"src": product.get(self.images_column, '').split(',')[0]} if product.get(self.images_column, '') else {},
                "attributes": [default_attr],
                "status": "publish",
                "purchasable": True
            }
            var_response = self.wc_upload_service.create_variation(product_id, variation_data)
            if var_response.status_code == 201:
                logger.info(f"Default variant '{default_attr['option']}' created successfully for product ID {product_id}.")
            else:
                logger.info(f"Error creating default variant '{default_attr['option']}']: {var_response.json()}")

    def create_variations(self, products, parent_id_map):
        """
        Create product variations.
        """
        counter_vr = 0
        for product in products:
            if product['type'] == 'variation':
                self.create_variation(product, parent_id_map)
                counter_vr += 1
                if counter_vr % 50 == 0:
                    print(f'\n{counter_vr} variants of products created.')
                    logger.info(f'\n{counter_vr} variants of products created.')

    def create_variation(self, product, parent_id_map):
        """
        Create a single product variation.
        """
        try:
            parent_sku = product['parent_id']
            if parent_sku + 'v' in parent_id_map:
                parent_id = parent_id_map[parent_sku + 'v']
                variation_data = {
                    "sku": product['sku'],
                    "regular_price": str(product.get('regular_price', '')),
                    "image": {"src": product.get(self.images_column, '').split(',')[0]} if product.get(self.images_column, '') else {},
                    "attributes": [{"name": attr['name'], "option": attr['options'][0] if attr['options'] else ""} for attr in product.get('attributes', [])],
                    "status": "publish",
                    "purchasable": True
                }
                response = self.wc_upload_service.create_variation(parent_id, variation_data)
                if response.status_code == 201:
                    logger.info(f"Variant '{product['name']}' created successfully for product ID {parent_id}.")
                else:
                    logger.info(f"Error creating variant '{product['name']}']: {response.json()}")
            else:
                logger.info(f"Parent product SKU '{parent_sku}' not found.")
        except Exception as e:
            logger.error(f"Error creating variant '{product['name']}': {e}")

    def create_simple_products(self, products):
        """
        Create simple products.
        """
        counter_s = 0
        for product in products:
            if product['type'] == 'simple':
                self.create_simple_product(product)
                counter_s += 1
                if counter_s % 50 == 0:
                    print(f'\n\n{counter_s} simple products created.')
                    logger.info(f'{counter_s} simple products created.')

    def create_simple_product(self, product):
        """
        Create a single simple product.
        """
        try:
            product.pop('parent_id', None)
            product['images'] = self.data_preparation_service.process_images(product.get(self.images_column, ''))
            response = self.wc_upload_service.create_product(product)
            if response.status_code == 201:
                logger.info(f"\nProduct '{product['name']}' created successfully.")
            else:
                logger.info(f"Error creating product '{product['name']}']: {response.json()}")
        except Exception as e:
            logger.error(f"Error creating simple product '{product['name']}': {e}")
