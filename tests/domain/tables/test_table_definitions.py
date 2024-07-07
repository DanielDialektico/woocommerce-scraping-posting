import pandas as pd
import pytest
from unittest.mock import patch
from src.common.utils import files_output_path
from src.config.config import WOOC_SAMPLE
from src.domain.tables import TableDefinitions

# Mock data for the CSV file and URLs
MOCK_CSV_COLUMNS = ['column1', 'column2', 'column3']
MOCK_URLS = ['http://example.com', 'http://example.org']

@patch('src.common.utils.files_output_path')
@patch('pandas.read_csv')
def test_product_table(mock_read_csv, mock_files_output_path):
    # Arrange
    mock_files_output_path.return_value = 'mock/path/to/sample.csv'
    mock_read_csv.return_value = pd.DataFrame(columns=MOCK_CSV_COLUMNS)

    # Act
    product_df = TableDefinitions.product_table()

    # Assert
    assert product_df.empty
    assert list(product_df.columns) == MOCK_CSV_COLUMNS

def test_urls_table():
    # Act
    urls_df = TableDefinitions.urls_table(MOCK_URLS)

    # Assert
    assert not urls_df.empty
    assert list(urls_df.columns) == ['URL']
    assert urls_df['URL'].tolist() == MOCK_URLS