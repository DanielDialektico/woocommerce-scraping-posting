import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from src.application.services import ImagesFactoryService

# Mock data for testing
MOCK_WOOC_DF = pd.DataFrame({
    'name': ['Product1', 'Product2'],
    'image_id/gallery_image_ids': ['image1.jpg', 'image2.jpg'],
    'sku': ['sku1', 'sku2'],
    'parent_id': ['', '']
})

MOCK_PATHS_DF = pd.DataFrame({
    'name': ['Product1', 'Product2'],
    'image_id': ['image1.jpg', 'image2.jpg'],
    'sku': ['sku1', 'sku2'],
    'parent_id': ['', ''],
    'route': ['mock/path/Product1/image1.jpg', 'mock/path/Product2/image2.jpg']
})

MOCK_IMAGE_URLS = [(0, 'http://example.com/image1.jpg'), (1, 'http://example.com/image2.jpg')]

@patch('src.application.services.images_factory_service.pd.read_csv')
@patch('src.application.services.images_factory_service.files_output_path')
@patch('src.application.services.images_factory_service.os.rename')
def test_create_paths_table(mock_rename, mock_files_output_path, mock_read_csv):
    # Arrange
    mock_files_output_path.side_effect = lambda *args: 'mock/path/' + '/'.join(args)
    mock_read_csv.return_value = MOCK_WOOC_DF
    service = ImagesFactoryService()

    # Act
    paths_df = service.create_paths_table()

    # Assert
    assert isinstance(paths_df, pd.DataFrame)
    assert 'route' in paths_df.columns
    assert len(paths_df) == 2
    mock_rename.assert_called()

@patch('src.application.services.images_factory_service.pd.read_csv')
@patch('src.application.services.images_factory_service.files_output_path')
def test_update_wc_table(mock_files_output_path, mock_read_csv):
    # Arrange
    mock_files_output_path.side_effect = lambda *args: 'mock/path/' + '/'.join(args)
    mock_read_csv.return_value = MOCK_WOOC_DF
    service = ImagesFactoryService()

    # Act
    updated_df = service.update_wc_table(MOCK_PATHS_DF, MOCK_IMAGE_URLS)

    # Assert
    assert isinstance(updated_df, pd.DataFrame)
    assert 'image_id/gallery_image_ids' in updated_df.columns
    assert updated_df.loc[updated_df['sku'] == 'sku1', 'image_id/gallery_image_ids'].values[0] == 'http://example.com/image1.jpg'

@patch('src.application.services.images_factory_service.pd.read_csv')
@patch('src.application.services.images_factory_service.files_output_path')
@patch('src.application.services.images_factory_service.pd.DataFrame.to_csv')
def test_save_updated_csv(mock_to_csv, mock_files_output_path, mock_read_csv):
    # Arrange
    mock_files_output_path.side_effect = lambda *args: 'mock/path/' + '/'.join(args)
    mock_read_csv.return_value = MOCK_WOOC_DF
    service = ImagesFactoryService()
    updated_df = service.update_wc_table(MOCK_PATHS_DF, MOCK_IMAGE_URLS)

    # Act
    service.save_updated_csv(updated_df)

    # Assert
    mock_to_csv.assert_called_once_with('mock/path/files\\tables/updated-wc_products.csv', index=False, encoding='utf-8')