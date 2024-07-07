import pytest
from unittest.mock import patch, MagicMock
from src.infrastructure.services.bs_crawling_service import BSCrawlingWebService

@patch('src.infrastructure.services.bs_crawling_service.requests.get')
def test_crawling_web(mock_get):
    # Arrange
    service = BSCrawlingWebService()
    html_content = '''
        <html>
            <body>
                <a href="https://www.petmarkt.com.mx/collections/all/products/product1">Product 1</a>
                <a href="https://www.petmarkt.com.mx/collections/all/products/product2">Product 2</a>
            </body>
        </html>
    '''
    mock_response = MagicMock()
    mock_response.content = html_content.encode('utf-8')  # Ensure content is bytes
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Act
    urls = service.crawling_web()

    # Assert
    expected_urls = [
        "https://www.petmarkt.com.mx/collections/all/products/product1",
        "https://www.petmarkt.com.mx/collections/all/products/product2"
    ]
    print(f"URLs: {urls}")
    assert isinstance(urls, list)
    assert all(url in urls for url in expected_urls)

def test_url_validator():
    # Arrange
    service = BSCrawlingWebService()
    valid_url = "https://www.petmarkt.com.mx/collections/all/products/product1"
    invalid_url = "https://www.petmarkt.com.mx/other/products/product3"
    domain = "www.petmarkt.com.mx"
    prefix = "https://www.petmarkt.com.mx/collections/all/products"

    # Act
    is_valid = service.url_validator(valid_url, domain, prefix)
    is_invalid = service.url_validator(invalid_url, domain, prefix)

    # Assert
    assert is_valid is True
    assert is_invalid is False

def test_update_prefix():
    # Arrange
    service = BSCrawlingWebService()
    initial_prefix = "https://www.petmarkt.com.mx/collections/all/products"
    service.prefix = initial_prefix

    # Act
    service.update_prefix()

    # Assert
    expected_prefix = "https://www.petmarkt.com.mx/collections/all/"
    assert service.prefix == expected_prefix