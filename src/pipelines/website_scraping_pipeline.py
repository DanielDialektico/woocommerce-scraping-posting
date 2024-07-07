import pandas as pd
import os
import requests
from src.config.config import SCRAPE_URLS, LOGGING_scraping_FILE
from src.common.utils import files_output_path, setup_logging
from src.domain.abstractions import WebsiteScrapingPipelineProtocol

# Initialize the logger
logger = setup_logging(LOGGING_scraping_FILE)

class WebsiteScrapingPipeline(WebsiteScrapingPipelineProtocol):
    """
    A pipeline class for scraping website data and saving the scrapped data and images.
    """
    
    def __init__(self, container):
        """
        Initialize the WebsiteScrapingPipeline with the given container.

        Args:
            container (object): The dependency injection container.
        """
        self.container = container
        self.tables_factory_service = container.config('tables_factory_service')
        self.scraping_service = container.config('scraping_service')

    def run(self):
        """
        Execute the web scraping pipeline.
        """
        print("\n\n-----Web scraping Stage-----\n")
        logger.info("Starting Web scraping Stage")

        urls_df = self.load_urls()
        if urls_df is None:
            return

        scrapped_dfs_list = self.scrape_urls(urls_df)

        self.save_scrapped_data(scrapped_dfs_list)

    def load_urls(self):
        """
        Load URLs from the CSV file.
        """
        try:
            urls_path = files_output_path('files\\tables', SCRAPE_URLS)
            return pd.read_csv(urls_path, encoding='latin1')
        except Exception as e:
            logger.error(f"Error reading URLs file: {e}")
            print(f"Error reading URLs file: {e}")
            return None

    def scrape_urls(self, urls_df):
        """
        Scrape data from the URLs in the DataFrame.
        """
        scrapped_dfs_list = []
        counter = 0

        for url in urls_df['Cleaned_URL']:
            scrapped_data = self.scrape_url(url)
            if scrapped_data:
                self.process_scrapped_data(scrapped_data, scrapped_dfs_list, url)
                counter += 1
                if counter % 50 == 0:
                    print(f'{counter} URLs have been scrapped.\n')
                    logger.info(f'{counter} URLs have been scrapped.')

        return scrapped_dfs_list

    def scrape_url(self, url):
        """
        Scrape a single URL.
        """
        try:
            return self.scraping_service.scrape(url)
        except Exception as e:
            logger.error(f"Error scraping URL {url}: {e}")
            print(f"Error scraping URL {url}: {e}")
            return None

    def process_scrapped_data(self, scrapped_data, scrapped_dfs_list, url):
        """
        Process the scrapped data and save images.
        """
        title = scrapped_data["title"]
        cleaned_title = title.replace(' ', '_')
        product_path = self.create_product_path(cleaned_title)

        image_names = self.download_images(scrapped_data["images"], product_path)

        try:
            scrapped_df = self.tables_factory_service.create_tables(
                scrapped_data["product_data"], title, scrapped_data["price"], 
                scrapped_data["description"], scrapped_data["brand"], 
                scrapped_data["tags"], image_names, scrapped_data["attribute"]
            )
            scrapped_dfs_list.append(scrapped_df)
        except Exception as e:
            logger.error(f"Error creating tables for URL {url}: {e}")
            print(f"Error creating tables for URL {url}: {e}")

    def create_product_path(self, cleaned_title):
        """
        Create the product path for saving images.
        """
        product_path = files_output_path('files\\images', cleaned_title)
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
                logger.error(f"Error downloading/saving image {img_url}: {e}")
                print(f"Error downloading/saving image {img_url}: {e}")

        return image_names

    def save_scrapped_data(self, scrapped_dfs_list):
        """
        Save the scrapped data.
        """
        if scrapped_dfs_list:
            try:
                all_scrapped_data = pd.concat(scrapped_dfs_list, ignore_index=True)
                self.tables_factory_service.save_products_csv(all_scrapped_data)
                path = files_output_path('files\\images', '')
                print(f'The images have been saved to {path}')
            except Exception as e:
                logger.error(f"Error saving concatenated data: {e}")
                print(f"Error saving concatenated data: {e}")
        else:
            print("No dataframes to concatenate and save.")
            logger.info("No dataframes to concatenate and save.")