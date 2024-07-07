# Import services from the application and infrastructure layers
from src.application.services import TablesFactoryService, URLsFactoryService, ImagesFactoryService, DataPreparationService
from src.infrastructure.services import BSScrapingService, WPImagesService, BSCrawlingWebService, WCUploadService
from src.config.ioc import IoCContainer

def ioc_config():
    """
    Configures the Inversion of Control (IoC) container by registering
    the necessary service instances.

    Returns:
        IoCContainer: The IoC container configured with the registered services.
    """
    # Create an instance of the IoC container
    container = IoCContainer()
    
    # Register services in the IoC container
    container.register('tables_factory_service', TablesFactoryService())
    container.register('scraping_service', BSScrapingService())
    container.register('urls_factory_service', URLsFactoryService())
    container.register('crawling_web_service', BSCrawlingWebService())
    container.register('images_factory_service', ImagesFactoryService())
    container.register('wp_images_service', WPImagesService())
    container.register('data_preparation_service', DataPreparationService())
    container.register('wc_upload_service', WCUploadService())
    
    # Return the configured IoC container
    return container
