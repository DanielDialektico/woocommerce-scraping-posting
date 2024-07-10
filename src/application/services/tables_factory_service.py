import pandas as pd
from src.domain.tables import TableDefinitions 
from src.config.config import SCRAPED_PRODUCTS_CSV, LOGGING_SCRAPING_FILE, SCRAPED_DESCRIPTIONS_CSV
from src.common.utils import files_output_path, setup_logging

class TablesFactoryService:
    
    def __init__(self):
        """
        Initializes the TablesFactoryService by loading the product DataFrame template.
        
        Expected input:
        - None
        
        Expected output:
        - None (initializes self.product_df)
        """
        self.logger = setup_logging(LOGGING_SCRAPING_FILE)
        self.product_df = TableDefinitions.product_table()

    def _create_variant_df(self, variant, title, brand, tags, parent_sku, image_name, attribute_name) -> pd.DataFrame:
        """
        Creates a DataFrame for a product variant.

        Expected input:
        - variant (dict): The variant data.
        - title (str): The product title.
        - brand (str): The product brand.
        - tags (list): The product tags.
        - parent_sku (str): The parent SKU.
        - image_name (str): The image name for the variant.
        - attribute_name (str): The attribute name.

        Expected output:
        - pd.DataFrame: DataFrame containing the variant product information.
        """
        variant_df = self.product_df.copy()
        sku = variant["sku"]
        price = variant["compare_at_price"] / 100  # Convert from cents
        variant_title = variant["public_title"]

        new_product = {
            'type': 'variation',
            'featured': False,
            'catalog_visibility': 'visible',
            'tax_status': 'none',
            'stock_status': 'instock',
            'backorders': 'no',
            'sold_individually': False,
            'sku': sku,
            'parent_id': parent_sku,
            'name': f"{title} - {variant_title}",
            'price': price,
            'regular_price': price,
            'tag_ids': ', '.join(tags),
            'image_id/gallery_image_ids': image_name,
            'brand': brand,
            'status': 'publish',
            'attributes': attribute_name,            
            'reviews_allowed': 1,
            'attributes.1': variant_title,
            'attributes.2': 1
        }

        for column in variant_df.columns:
            if column not in new_product:
                new_product[column] = ''

        # Create a DataFrame with a single row using new_product
        new_product_df = pd.DataFrame([new_product])

        # Use concat only if variant_df is not empty
        if not variant_df.empty:
            variant_df = pd.concat([variant_df, new_product_df], ignore_index=True)
        else:
            variant_df = new_product_df

        return variant_df

    def _create_parent_df(self, title, sku, price, description, brand, tags, attribute_name, attribute_values, gallery_images) -> pd.DataFrame:
        """
        Creates a DataFrame for a parent product.

        Expected input:
        - title (str): The product title.
        - sku (str): The SKU.
        - price (float): The price.
        - description (str): The product description.
        - brand (str): The brand.
        - tags (list): The product tags.
        - attribute_name (str): The attribute name.
        - attribute_values (list): The attribute values.
        - gallery_images (list): The gallery images.

        Expected output:
        - pd.DataFrame: DataFrame containing the parent product information.
        """
        parent_df = self.product_df.copy()

        new_product = {
            'type': 'variable',
            'featured': True,
            'catalog_visibility': 'visible',
            'tax_status': 'none',
            'stock_status': 'instock',
            'backorders': 'no',
            'sold_individually': False,
            'sku': sku,
            'name': title,
            'price': price,
            'regular_price': price,
            'description': description,
            'tag_ids': ', '.join(tags),
            'image_id/gallery_image_ids': ', '.join(gallery_images),
            'brand': brand,
            'status': 'publish',
            'reviews_allowed': 1,
            'attributes': attribute_name,
            'attributes.1': ', '.join(attribute_values),
            'default_attributes': attribute_values[0] if attribute_values else '',
            'attributes.2': 1
        }

        for column in parent_df.columns:
            if column not in new_product:
                new_product[column] = ''

        # Create a DataFrame with a single row using new_product
        new_product_df = pd.DataFrame([new_product])

        # Use concat only if parent_df is not empty
        if not parent_df.empty:
            parent_df = pd.concat([parent_df, new_product_df], ignore_index=True)
        else:
            parent_df = new_product_df

        return parent_df

    def _create_simple_df(self, title, sku, price, description, brand, tags, image_name, gallery_images) -> pd.DataFrame:
        """
        Creates a DataFrame for a simple product.

        Expected input:
        - title (str): The product title.
        - sku (str): The SKU.
        - price (float): The price.
        - description (str): The product description.
        - brand (str): The brand.
        - tags (list): The product tags.
        - image_name (str): The image name.
        - gallery_images (list): The gallery images.

        Expected output:
        - pd.DataFrame: DataFrame containing the simple product information.
        """
        simple_df = self.product_df.copy()

        new_product = {
            'type': 'simple',
            'featured': True,
            'catalog_visibility': 'visible',
            'tax_status': 'none',
            'stock_status': 'instock',
            'backorders': 'no',
            'sold_individually': False,
            'sku': sku,
            'name': title,
            'price': price,
            'regular_price': price,
            'description': description,
            'tag_ids': ', '.join(tags),
            'image_id/gallery_image_ids': ', '.join([image_name] + gallery_images[1:]) if gallery_images else '',
            'gallery_image_ids': ', '.join(gallery_images[1:]) if len(gallery_images) > 1 else '',
            'brand': brand,
            'status': 'publish',
            'reviews_allowed': 1
        }

        for column in simple_df.columns:
            if column not in new_product:
                new_product[column] = ''

        # Create a DataFrame with a single row using new_product
        new_product_df = pd.DataFrame([new_product])

        # Use concat only if simple_df is not empty
        if not simple_df.empty:
            simple_df = pd.concat([simple_df, new_product_df], ignore_index=True)
        else:
            simple_df = new_product_df

        return simple_df        

    def create_tables(self, product_data, title, price, description, brand, tags, image_names, attribute_name) -> pd.DataFrame:
        """
        Creates tables for products based on the given data.

        Expected input:
        - product_data (dict): The product data.
        - title (str): The product title.
        - price (float): The price.
        - description (str): The product description.
        - brand (str): The brand.
        - tags (list): The product tags.
        - image_names (list): The image names.
        - attribute_name (str): The attribute name.

        Expected output:
        - pd.DataFrame: DataFrame containing the product information.
        """
        self.logger.info("Starting to create tables for product.")
        # Process product
        if "variants" in product_data["product"] and len(product_data["product"]["variants"]) > 1:
            attribute_values = [variant["public_title"] for variant in product_data["product"]["variants"] if variant["public_title"]]
            parent_sku = product_data["product"]["variants"][0]["sku"]
            wooc_df = self._create_parent_df(title, parent_sku, price, description, brand, tags, attribute_name, attribute_values, image_names)
            for idx, variant in enumerate(product_data["product"]["variants"][1:]):  # Start from the second variant
                image_name = image_names[idx + 1] if (idx + 1) < len(image_names) else None
                variant_df = self._create_variant_df(variant, title, brand, tags, parent_sku, image_name, attribute_name)
                wooc_df = pd.concat([wooc_df, variant_df], ignore_index=True)
                self.logger.info(f"Processed variant {idx + 1}/{len(product_data['product']['variants']) - 1}.")
        else:
            # Single product without variants
            variant = product_data["product"]["variants"][0]
            sku = variant["sku"]
            image_name = image_names[0] if len(image_names) > 0 else None
            wooc_df = self._create_simple_df(title, sku, price, description, brand, tags, image_name, image_names)
            self.logger.info("Processed single product without variants.")

        # Ensure all original CSV columns are in the DataFrame
        for column in self.product_df.columns:
            if column not in wooc_df.columns:
                wooc_df[column] = ''

        # Replace NaN with empty strings
        wooc_df = wooc_df.fillna('')

        # Infer objects to avoid future warnings
        wooc_df = wooc_df.infer_objects(copy=False)

        # Reorder columns to match the sample CSV
        wooc_df = wooc_df[self.product_df.columns]

        # Replace .1, .2, and .3 in column names
        wooc_df.columns = wooc_df.columns.str.replace(r'\.1', '', regex=True)
        wooc_df.columns = wooc_df.columns.str.replace(r'\.2', '', regex=True)
        wooc_df.columns = wooc_df.columns.str.replace(r'\.3', '', regex=True)
        
        self.logger.info("Finished creating tables for product.")
        return wooc_df
    
    def save_products_csv(self, df: pd.DataFrame) -> None:
        """
        Saves the product DataFrame to a CSV file.

        Expected input:
        - df (pd.DataFrame): The product DataFrame to save.

        Expected output:
        - None (saves the DataFrame to a CSV file).
        """
        df_output_path = files_output_path('files\\tables', SCRAPED_PRODUCTS_CSV)
        df_desc_output_path = files_output_path('files\\tables', SCRAPED_DESCRIPTIONS_CSV)
       
        df_desc = df[['description']]
        df = df.drop(columns=['description'])
    
        df_desc.to_csv(df_desc_output_path, index=False, encoding='utf-8')
        df.to_csv(df_output_path, index=False, encoding='utf-8')

        self.logger.info(f'\n{len(df)} products have been saved to {df_output_path}')
        print(f'{len(df)} products have been saved to {df_output_path}')

        self.logger.info(f'\n{len(df)} product descriptions have been saved to {df_desc_output_path}')
        print(f'{len(df)} product descriptions have been saved to {df_desc_output_path}')        