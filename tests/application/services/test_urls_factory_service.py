import pandas as pd
import pytest
from unittest.mock import patch
from src.application.services import URLsFactoryService

# Mock data for testing
MOCK_URLS = [
    'https://www.example.com/collections/all/products/product1?variant=123',
    'https://www.example.com/collections/all/products/product2?variant=456',
    'https://www.example.com/collections/all/products/product1?variant=123',  # Duplicate for testing
    'https://www.other.com/collections/other/products/product3'
]

@patch('src.application.services.urls_factory_service.files_output_path')
@patch('src.application.services.urls_factory_service.TableDefinitions.urls_table')
def test_filter_urls(mock_urls_table, mock_files_output_path):
    # Arrange
    mock_files_output_path.return_value = 'mock/path'
    mock_urls_table.return_value = pd.DataFrame({'URL': MOCK_URLS})
    service = URLsFactoryService()

    # Act
    filtered_df = service.filter_urls(MOCK_URLS)

    # Assert
    assert isinstance(filtered_df, pd.DataFrame)
    assert 'Cleaned_URL' in filtered_df.columns
    assert len(filtered_df) == 2  # Should filter out the non-matching URL and duplicate

@patch('src.application.services.urls_factory_service.files_output_path')
@patch('src.application.services.urls_factory_service.pd.DataFrame.to_csv')
def test_save_urls_csv(mock_to_csv, mock_files_output_path):
    # Arrange
    mock_files_output_path.return_value = 'mock/path/files/tables/product-urls.csv'
    service = URLsFactoryService()
    test_df = pd.DataFrame({'URL': ['https://www.example.com/collections/all/products/product1']})

    # Act
    service.save_urls_csv(test_df)

    # Assert
    mock_to_csv.assert_called_once_with('mock/path/files/tables/product-urls.csv', index=False, encoding='latin1')