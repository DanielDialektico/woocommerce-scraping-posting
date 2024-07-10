import os
from typing import List
import pandas as pd
from src.common.utils import files_output_path, setup_logging
from src.config.config import SCRAPED_PRODUCTS_CSV, UPDATED_PRODUCTS_CSV, LOGGING_IMAGES_FILE
from src.domain.abstractions import ImagesFactoryServiceProtocol

class ImagesFactoryService(ImagesFactoryServiceProtocol):
    def __init__(self):
        """
        Initializes the ImagesFactoryService.

        Loads the WooCommerce DataFrame from a CSV file and sets the base path for images.
        """
        self.wooc_df = pd.read_csv(files_output_path('files\\tables', SCRAPED_PRODUCTS_CSV), encoding='latin1')
        self.images_base_path = files_output_path('files\\images', '')
        self.logger = setup_logging(LOGGING_IMAGES_FILE)


    def create_paths_table(self) -> pd.DataFrame:
        """
        Creates a table of image paths based on the WooCommerce DataFrame.

        Expected input:
        - None (uses self.wooc_df loaded during initialization).

        Expected output:
        - pd.DataFrame: DataFrame containing columns 'name', 'image_id/gallery_image_ids', 'sku', 'parent_id', 'route'.

        The function:
        1. Copies relevant columns from the WooCommerce DataFrame.
        2. Adjusts 'name' values for rows with 'parent_id'.
        3. Splits 'image_id/gallery_image_ids' into separate rows.
        4. Creates the 'route' column with the image paths.
        5. Renames images and updates the 'route' column.
        6. Removes duplicate paths and returns the updated DataFrame.
        """
        self.logger.info("Initialized ImagesFactoryService.")        
        self.logger.info("Creating paths table.")
        paths_df = self.wooc_df[['name', 'image_id/gallery_image_ids', 'sku', 'parent_id']].copy()

        for index, row in paths_df.iterrows():
            if row['parent_id'] != '':
                parent_name = paths_df.loc[paths_df['sku'] == row['parent_id'], 'name'].values
                if len(parent_name) > 0:
                    paths_df.at[index, 'name'] = parent_name[0]
                    self.logger.debug(f"Updated name for SKU {row['sku']} to parent name {parent_name[0]}.")

        paths_df = paths_df.assign(image_id=paths_df['image_id/gallery_image_ids'].str.split(',')).explode('image_id')
        paths_df['route'] = paths_df.apply(lambda row: os.path.join(self.images_base_path, row['name'].replace(' ', '_'), row['image_id'].strip()), axis=1)
        paths_df = paths_df.drop_duplicates(subset=['route'], keep='last').reset_index(drop=True)

        for index, row in paths_df.iterrows():
            old_path = row['route']
            new_image_name = f"{os.path.splitext(row['image_id'])[0]}_{row['sku']}.jpg"
            new_path = os.path.join(self.images_base_path, row['name'].replace(' ', '_'), new_image_name)
            os.rename(old_path, new_path)
            paths_df.at[index, 'route'] = new_path
            self.logger.debug(f"Renamed image {old_path} to {new_path}.")

        self.logger.info("Paths table created successfully.")
        return paths_df    

    def update_wc_table(self, paths_df: pd.DataFrame, image_urls: List[str]) -> pd.DataFrame:
        """
        Updates the WooCommerce DataFrame with image URLs.

        Expected input:
        - paths_df (pd.DataFrame): DataFrame containing columns 'name', 'image_id', 'sku', 'parent_id', 'route'.
        - image_urls (List[str]): List of image URLs.

        Expected output:
        - pd.DataFrame: Updated WooCommerce DataFrame with new image URLs.

        The function:
        1. Copies the WooCommerce DataFrame.
        2. Adds image URLs to the paths DataFrame.
        3. Maps SKUs to their respective URLs.
        4. Updates the 'image_id/gallery_image_ids' column in the original DataFrame with the new URLs.
        5. Returns the updated DataFrame.
        """
        self.logger.info("Updating WooCommerce table with image URLs.")
        df = self.wooc_df.copy()
        paths_df['image_url'] = [url for _, url in sorted(image_urls, key=lambda x: x[0])]
        sku_to_urls = paths_df.groupby('sku')['image_url'].apply(lambda urls: ', '.join(filter(None, urls))).to_dict()

        for sku, urls in sku_to_urls.items():
            df.loc[df['sku'] == sku, 'image_id/gallery_image_ids'] = urls
            self.logger.debug(f"Updated SKU {sku} with URLs: {urls}")

        self.logger.info("WooCommerce table updated successfully.")
        return df    

    def save_updated_csv(self, df: pd.DataFrame) -> None:
        """
        Saves the updated WooCommerce DataFrame to a CSV file.

        Expected input:
        - df (pd.DataFrame): The updated WooCommerce DataFrame.

        Expected output:
        - None (writes the DataFrame to a CSV file).

        The function:
        1. Defines the output path for the updated CSV file.
        2. Writes the DataFrame to the CSV file with the specified encoding.
        3. Logs the completion of the save operation.
        """

        output_path = files_output_path('files\\tables', UPDATED_PRODUCTS_CSV)
        df.to_csv(output_path, index=False, encoding='latin1')
        self.logger.info(f"Updated CSV with image URLs has been saved to {output_path}")