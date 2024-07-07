import pytest
from unittest.mock import MagicMock
from src.pipelines.products_uploading_pipeline import ProductsUploadingPipeline
from src.config.config import UPDATED_PRODUCTS_CSV, WC_URL

@pytest.fixture
def container():
    mock_container = MagicMock()
    mock_container.config = MagicMock()
    return mock_container

def test_run_with_fixture(container):
    # Arrange
    mock_data_preparation_service = MagicMock()
    mock_wc_upload_service = MagicMock()
    container.config.side_effect = lambda name: {
        'data_preparation_service': mock_data_preparation_service,
        'wc_upload_service': mock_wc_upload_service
    }[name]

    mock_products = [
        {'type': 'variable', 'sku': 'sku1', 'name': 'Product 1', 'image_id/gallery_image_ids': 'image1', 'regular_price': '100'},
        {'type': 'variation', 'sku': 'sku2', 'parent_id': 'sku1', 'name': 'Product 2', 'image_id/gallery_image_ids': 'image2', 'regular_price': '50'},
        {'type': 'simple', 'sku': 'sku3', 'name': 'Product 3', 'image_id/gallery_image_ids': 'image3', 'regular_price': '25'}
    ]
    mock_data_preparation_service.prepare_data.return_value = mock_products
    mock_wc_upload_service.create_product.return_value = MagicMock(status_code=201, json=lambda: {'id': 1})
    mock_wc_upload_service.create_variation.return_value = MagicMock(status_code=201, json=lambda: {'id': 2})

    pipeline = ProductsUploadingPipeline(container)

    # Act
    pipeline.run()

    # Assert
    mock_data_preparation_service.prepare_data.assert_called_once_with(UPDATED_PRODUCTS_CSV)
    assert mock_wc_upload_service.create_product.call_count == 2
    assert mock_wc_upload_service.create_variation.call_count == 1
    print(f"\nProducts have been created in {WC_URL}.")
