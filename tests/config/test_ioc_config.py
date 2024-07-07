import pytest
from src.config.ioc import IoCContainer
from src.config.ioc import ioc_config
from src.application.services import TablesFactoryService, URLsFactoryService, ImagesFactoryService, DataPreparationService
from src.infrastructure.services import BSScrapingService, WPImagesService, BSCrawlingWebService, WCUploadService

def test_ioc_config():
    # Act
    container = ioc_config()

    # Assert
    assert isinstance(container, IoCContainer)
    assert isinstance(container.config('tables_factory_service'), TablesFactoryService)
    assert isinstance(container.config('scraping_service'), BSScrapingService)
    assert isinstance(container.config('urls_factory_service'), URLsFactoryService)
    assert isinstance(container.config('crawling_web_service'), BSCrawlingWebService)
    assert isinstance(container.config('images_factory_service'), ImagesFactoryService)
    assert isinstance(container.config('wp_images_service'), WPImagesService)
    assert isinstance(container.config('data_preparation_service'), DataPreparationService)
    assert isinstance(container.config('wc_upload_service'), WCUploadService)