import os
from src.common.utils import setup_logging
from src.config.config import LOGGING_CRAWLING_FILE
from src.domain.abstractions import WebsiteCrawlingPipelineProtocol

# Initialize the logger
logger = setup_logging(LOGGING_CRAWLING_FILE)

class WebsiteCrawlingPipeline(WebsiteCrawlingPipelineProtocol):
    """
    A pipeline class for executing web crawling, URL filtering, and saving URLs.
    """

    def __init__(self, container):
        """
        Initialize the WebsiteCrawlingPipeline with the given container.

        Args:
            container (object): The dependency injection container.
        """
        self.container = container
        self.crawling_service = container.config('crawling_web_service')
        self.filtering_service = container.config('urls_factory_service')

    def run(self):
        """
        Execute crawling, filtering, and saving of URLs in a single function.

        Expected input:
        - None

        Expected output:
        - None (performs crawling, filtering, and saving URLs)
        """
        print("\n-----Web Crawling and URLs Saving Stage-----\n")
        logger.info("Starting Web Crawling and URLs Saving Stage")

        # Perform web crawling
        try:
            urls = self.crawling_service.crawling_web()
            while not urls:
                print("Empty URLs list, trying with immediate level:")
                logger.info("Empty URLs list, testing with immediate level:")            
                self.crawling_service.update_prefix()
                urls = self.crawling_service.crawling_web()

            if not urls:
                error_message = "List of empty URLs for all versions of the prefix, try with another CATEGORIES_URL in config.py."
                print(error_message)
                logger.error(error_message)
                raise ValueError(error_message)

            print("\nFiltering URLs with the selected URL structure...\n")  
            logger.info("Filtering URLs with the selected URL structure...")
            df_unique = self.filtering_service.filter_urls(urls)

            if df_unique.empty:
                error_message = "URL not found in table, try with another CATEGORIES_URL in config.py."
                print(error_message)
                logger.error(error_message)
                raise ValueError(error_message)

            self.filtering_service.save_urls_csv(df_unique)

        except Exception as e:
            logger.error(f"An error occurred during the pipeline run: {e}")
            print(f"An error occurred during the pipeline run: {e}")