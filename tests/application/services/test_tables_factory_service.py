import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from src.application.services import TablesFactoryService

# Mock data for testing
MOCK_PRODUCT_DATA = {
    "product": {
        "variants": [
            {"sku": "sku1", "compare_at_price": 1000, "public_title": "Variant1"},
            {"sku": "sku2", "compare_at_price": 2000, "public_title": "Variant2"}
        ]
    }
}
MOCK_TITLE = "Product Title"
MOCK_PRICE = 10.0
MOCK_DESCRIPTION = "Product Description"
MOCK_BRAND = "Product Brand"
MOCK_TAGS = ["tag1", "tag2"]
MOCK_IMAGE_NAMES = ["image1.jpg", "image2.jpg"]
MOCK_ATTRIBUTE_NAME = "Color"

@patch('src.application.services.tables_factory_service.TableDefinitions.product_table')
@patch('src.application.services.tables_factory_service.files_output_path')
@patch('src.application.services.tables_factory_service.setup_logging')
def test_create_tables(mock_setup_logging, mock_files_output_path, mock_product_table):
    # Arrange
    mock_files_output_path.return_value = 'mock/path'
    mock_product_table.return_value = pd.DataFrame(columns=[
        'type', 'featured', 'catalog_visibility', 'tax_status', 'stock_status',
        'backorders', 'sold_individually', 'sku', 'parent_id', 'name', 'price',
        'regular_price', 'description', 'tag_ids', 'image_id/gallery_image_ids',
        'brand', 'status', 'reviews_allowed', 'attributes', 'attributes.1',
        'default_attributes', 'attributes.2'
    ])
    service = TablesFactoryService()

    # Act
    result_df = service.create_tables(
        product_data=MOCK_PRODUCT_DATA,
        title=MOCK_TITLE,
        price=MOCK_PRICE,
        description=MOCK_DESCRIPTION,
        brand=MOCK_BRAND,
        tags=MOCK_TAGS,
        image_names=MOCK_IMAGE_NAMES,
        attribute_name=MOCK_ATTRIBUTE_NAME
    )

    # Assert
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty
    assert 'sku' in result_df.columns
    assert result_df.loc[0, 'sku'] == "sku1"

@patch('src.application.services.tables_factory_service.files_output_path')
@patch('src.application.services.tables_factory_service.pd.DataFrame.to_csv')
def test_save_products_csv(mock_to_csv, mock_files_output_path):
    # Arrange
    mock_files_output_path.return_value = 'mock/path/files/tables/scraped-products.csv'
    service = TablesFactoryService()
    test_df = pd.DataFrame({'sku': ['sku1', 'sku2']})

    # Act
    service.save_products_csv(test_df)

    # Assert
    mock_to_csv.assert_called_once_with('mock/path/files/tables/scraped-products.csv', index=False, encoding='latin1')
