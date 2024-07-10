import pandas as pd
import os
import requests
import re
from src.config.config import PRODUCT_URLS_CSV, LOGGING_SCRAPING_FILE
from src.common.utils import files_output_path, setup_logging
from src.domain.abstractions import WebsiteScrapingPipelineProtocol

class WebsiteScrapingPipeline(WebsiteScrapingPipelineProtocol):
    """
    A pipeline class for scraping website data and saving the scraped data and images.
    """
    
    def __init__(self, container):
        """
        Initialize the WebsiteScrapingPipeline with the given container.

        Args:
            container (object): The dependency injection container.
        """
        self.logger = setup_logging(LOGGING_SCRAPING_FILE)
        self.container = container
        self.tables_factory_service = container.config('tables_factory_service')
        self.scraping_service = container.config('scraping_service')

    def run(self):
        """
        Execute the web scraping pipeline.
        """
        print("\n\n-----Web scraping Stage-----\n")
        self.logger.info("Starting Web scraping Stage")

        urls_df = self.load_urls()
        if urls_df is None:
            return

        scraped_dfs_list = self.scrape_urls(urls_df)

        self.save_scraped_data(scraped_dfs_list)

    def load_urls(self):
        """
        Load URLs from the CSV file.
        """
        try:
            urls_path = files_output_path('files\\tables', PRODUCT_URLS_CSV)
            return pd.read_csv(urls_path, encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Error reading URLs file: {e}")
            print(f"Error reading URLs file: {e}")
            return None

    def scrape_urls(self, urls_df):
        """
        Scrape data from the URLs in the DataFrame.
        """
        scraped_dfs_list = []
        counter = 0

        for url in urls_df['Cleaned_URL']:
            scraped_data = self.scrape_url(url)
            if scraped_data:
                self.process_scraped_data(scraped_data, scraped_dfs_list, url)
                counter += 1
                if counter % 50 == 0:
                    print(f'{counter} URLs have been scraped.\n')
                    self.logger.info(f'{counter} URLs have been scraped.')

        return scraped_dfs_list

    def scrape_url(self, url):
        """
        Scrape a single URL.
        """
        try:
            return self.scraping_service.scrape(url)
        except Exception as e:
            self.logger.error(f"Error scraping URL {url}: {e}")
            print(f"Error scraping URL {url}: {e}")
            return None

    def process_scraped_data(self, scraped_data, scraped_dfs_list, url):
        """
        Process the scraped data and save images.
        """
        title = scraped_data["title"]
        cleaned_title = title.replace(' ', '_')
        product_path = self.create_product_path(cleaned_title)

        image_names = self.download_images(scraped_data["images"], product_path)

        try:
            scraped_df = self.tables_factory_service.create_tables(
                scraped_data["product_data"], title, scraped_data["price"], 
                scraped_data["description"], scraped_data["brand"], 
                scraped_data["tags"], image_names, scraped_data["attribute"]
            )
            scraped_dfs_list.append(scraped_df)
        except Exception as e:
            self.logger.error(f"Error creating tables for URL {url}: {e}")
            print(f"Error creating tables for URL {url}: {e}")

    def create_product_path(self, cleaned_title: str) -> str:
        """
        Create the product path for saving images.
        """
        cleaned_title = re.sub(r'[<>:"/\\|?*]', '_', cleaned_title)
        base_path = os.path.join('files', 'images')
        max_length = 220 - len(os.path.abspath(base_path)) - 1

        if len(cleaned_title) > max_length:
            cleaned_title = cleaned_title[:max_length]

        product_path = os.path.join(base_path, cleaned_title)
        
        if not os.path.exists(product_path):
            os.makedirs(product_path)

        return product_path    


    def download_images(self, images, product_path):
        """
        Download and save images.
        """
        image_names = []
        for idx, img in enumerate(images, start=1):
            img_url = img['src']
            if img_url.startswith("//"):
                img_url = "https:" + img_url

            try:
                img_data = requests.get(img_url).content
                full_path = os.path.join(product_path, f'product_image_{idx}.jpg')
                with open(full_path, 'wb') as handler:
                    handler.write(img_data)
                image_names.append(f'product_image_{idx}.jpg')
            except Exception as e:
                self.logger.error(f"Error downloading/saving image {img_url}: {e}")
                print(f"Error downloading/saving image {img_url}: {e}")

        return image_names

    def save_scraped_data(self, scraped_dfs_list):
        """
        Save the scraped data.
        """
        if scraped_dfs_list:
            try:
                all_scraped_data = pd.concat(scraped_dfs_list, ignore_index=True)
                self.tables_factory_service.save_products_csv(all_scraped_data)
                path = files_output_path('files\\images', '')
                print(f'The images have been saved to {path}')
            except Exception as e:
                self.logger.error(f"Error saving concatenated data: {e}")
                print(f"Error saving concatenated data: {e}")
        else:
            print("No dataframes to concatenate and save.")
            self.logger.info("No dataframes to concatenate and save.")