import pytest
from unittest.mock import patch, MagicMock
from src.infrastructure.services.bs_scraping_service import BSScrapingService

@patch('src.infrastructure.services.bs_scraping_service.requests.get')
def test_scrape(mock_get):
    # Arrange
    service = BSScrapingService()
    url = "https://www.example.com/product"
    
    html_content = '''
        <html>
            <body>
                <section id="shopify-section-static-product">
                    <article>
                        <div class="product-main">
                            <div class="product-details">
                                <h1>Product Title</h1>
                                <div class="price">$123.45</div>
                                <div class="product-vendor">
                                    <a title="Brand Name">Brand</a>
                                </div>
                            </div>
                        </div>
                        <div class="product-description rte">Product Description</div>
                    </article>
                </section>
                <script data-section-type="static-product">{"product": {"tags": ["tag1", "tag2"]}}</script>
                <label class="form-field-title">Attribute Name</label>
                <img data-rimg="lazy" src="https://www.example.com/image1.jpg">
                <img data-rimg="lazy" src="https://www.example.com/image2.jpg">
            </body>
        </html>
    '''
    mock_response = MagicMock()
    mock_response.content = html_content.encode('utf-8')  # Ensure content is bytes
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Act
    result = service.scrape(url)

    # Assert
    expected_keys = {"title", "price", "brand", "description", "tags", "product_data", "attribute", "images"}
    assert isinstance(result, dict)
    assert set(result.keys()) == expected_keys

    # Additional check to ensure the types of the values are correct
    assert isinstance(result["title"], str)
    assert isinstance(result["price"], str)
    assert isinstance(result["brand"], str)
    assert isinstance(result["description"], str)
    assert isinstance(result["tags"], list)
    assert isinstance(result["product_data"], dict)
    assert isinstance(result["attribute"], str)
    assert isinstance(result["images"], list)
