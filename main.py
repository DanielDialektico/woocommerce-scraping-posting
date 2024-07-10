# Import the necessary configurations and pipeline classes
from src.config.ioc import ioc_config
from src.pipelines import WebsiteCrawlingPipeline, WebsiteScrapingPipeline, ImagesUploadPipeline, ProductsUploadingPipeline

def main():
    # Initialize the dependency injection container
    container = ioc_config()
    
    # Create instances of the pipelines with the container
    website_crawling_pipeline = WebsiteCrawlingPipeline(container)
    website_scraping_pipeline = WebsiteScrapingPipeline(container)
    images_upload_pipeline = ImagesUploadPipeline(container)
    products_uploading_pipeline = ProductsUploadingPipeline(container)

    # ----Run the pipelines in sequence

    # Run the website crawling pipeline to crawl product URLs.
    #website_crawling_pipeline.run()
    
    # Run the website scraping pipeline to scrape data and images from the website
    website_scraping_pipeline.run()
    
    # Run the images upload pipeline to upload scraped images
    images_upload_pipeline.run()
    
    # Run the products uploading pipeline to create products in WooCommerce with the scraped data and images
    products_uploading_pipeline.run()

if __name__ == "__main__":
    main()
