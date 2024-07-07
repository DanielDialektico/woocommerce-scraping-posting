
import pandas as pd
import pytest
from unittest.mock import patch
from src.application.services import DataPreparationService

def test_convert_attributes():
    service = DataPreparationService()
    row = pd.Series({
        'attribute_name': 'Color',
        'attribute_options': 'Red, Blue, Green',
        'attribute_visible': 'True',
        'attribute_variation': 'True',
        'default_attributes': 'Red'
    })
    result = service._convert_attributes(row)
    assert 'attributes' in result
    assert isinstance(result['attributes'], list)
    assert len(result['attributes']) == 1
    assert result['attributes'][0]['name'] == 'Color'
    assert result['attributes'][0]['options'] == ['Red', 'Blue', 'Green']
    assert result['attributes'][0]['visible'] is True
    assert result['attributes'][0]['variation'] is True
    assert 'default_attributes' in result
    assert isinstance(result['default_attributes'], list)
    assert len(result['default_attributes']) == 1
    assert result['default_attributes'][0]['name'] == 'Color'
    assert result['default_attributes'][0]['option'] == 'Red'

@patch('src.application.services.data_preparation_service.files_output_path')
@patch('pandas.read_csv')
def test_prepare_data(mock_read_csv, mock_files_output_path):
    mock_files_output_path.return_value = 'mock/path/to/sample.csv'
    mock_read_csv.return_value = pd.DataFrame({
        'attributes': ['Color'],
        'attributes.1': ['Red, Blue, Green'],
        'default_attributes': ['Red'],
        'attributes.2': ['True'],
        'attributes.3': ['True']
    })
    service = DataPreparationService()
    result = service.prepare_data('mock.csv')
    assert isinstance(result, list)
    assert len(result) == 1
    assert 'attribute_name' in result[0]
    assert 'attributes' in result[0]
    assert isinstance(result[0]['attributes'], list)
    assert len(result[0]['attributes']) == 1

def test_process_images():
    service = DataPreparationService()
    image_urls = 'http://example.com/image1.jpg, http://example.com/image2.jpg'
    result = service.process_images(image_urls)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]['src'] == 'http://example.com/image1.jpg'
    assert result[1]['src'] == 'http://example.com/image2.jpg'

