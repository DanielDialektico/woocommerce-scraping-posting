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
@patch('src.common.utils.logging.FileHandler')
def test_setup_logging(mock_file_handler, mock_get_logger, mock_makedirs, mock_files_output_path, tmpdir):
    # Arrange
    service_name = 'test_service'
    log_path = os.path.join(tmpdir, 'logs', service_name)
    mock_files_output_path.return_value = log_path
    mock_logger = MagicMock()
    mock_handler = MagicMock()
    mock_get_logger.return_value = mock_logger
    mock_file_handler.return_value = mock_handler
    mock_logger.hasHandlers.return_value = False  # Simulate logger without handlers

    # Act
    logger = setup_logging(service_name)

    # Assert
    mock_makedirs.assert_called_once_with(os.path.dirname(log_path), exist_ok=True)
    mock_file_handler.assert_called_once_with(log_path)
    mock_handler.setFormatter.assert_called_once()  # Check that setFormatter was called
    mock_logger.addHandler.assert_called_once_with(mock_handler)
    mock_logger.setLevel.assert_called_once_with(logging.DEBUG)
    mock_get_logger.assert_called_once_with(service_name)
    assert logger == mock_logger