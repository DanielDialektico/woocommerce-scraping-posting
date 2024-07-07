import os
import logging
import pytest
from unittest.mock import patch, MagicMock
from src.common.utils import files_output_path, setup_logging

def test_files_output_path(tmpdir):
    # Arrange
    directory = 'test_dir'
    filename = 'test_file.txt'
    expected_path = os.path.join(tmpdir, directory, filename)

    # Act
    with patch('src.common.utils.os.path.abspath', return_value=tmpdir):
        output_path = files_output_path(directory, filename)

    # Assert
    assert output_path == expected_path
    assert os.path.exists(os.path.dirname(output_path))

@patch('src.common.utils.files_output_path')
@patch('src.common.utils.os.makedirs')
@patch('src.common.utils.logging.getLogger')
@patch('src.common.utils.logging.basicConfig')
def test_setup_logging(mock_basic_config, mock_get_logger, mock_makedirs, mock_files_output_path, tmpdir):
    # Arrange
    service_name = 'test_service'
    log_path = os.path.join(tmpdir, 'logs', service_name)
    mock_files_output_path.return_value = log_path
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    # Act
    logger = setup_logging(service_name)

    # Assert
    mock_basic_config.assert_called_once_with(
        filename=log_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    mock_get_logger.assert_called_once_with(service_name)
    assert logger == mock_logger