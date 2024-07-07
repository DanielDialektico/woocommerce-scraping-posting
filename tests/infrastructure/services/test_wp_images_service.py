import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.infrastructure.services.wp_images_service import WPImagesService

def test_upload_image():
    # Arrange
    service = WPImagesService()
    image_path = 'test_image.jpg'
    expected_url = 'https://example.com/media/test_image.jpg'
    mock_response = MagicMock()
    mock_response.json.return_value = {'source_url': expected_url}
    mock_response.raise_for_status = MagicMock()

    with patch('builtins.open', mock_open(read_data=b'file_content')), \
         patch('src.infrastructure.services.wp_images_service.requests.post', return_value=mock_response) as mock_post:
        # Act
        result = service.upload_image(image_path)

        # Assert
        mock_post.assert_called_once()
        assert result == expected_url