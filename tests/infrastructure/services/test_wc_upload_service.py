import pytest
from unittest.mock import patch, MagicMock
from src.infrastructure.services.wc_upload_service import WCUploadService

def test_create_product():
    # Arrange
    service = WCUploadService()
    product_data = {
        "name": "Test Product",
        "type": "simple",
        "regular_price": "19.99",
        "description": "Test product description"
    }
    response_data = {"id": 123, "name": "Test Product"}
    
    with patch.object(service.wcapi, 'post', return_value=MagicMock(status_code=201, json=lambda: response_data)) as mock_post:
        # Act
        response = service.create_product(product_data)

        # Assert
        mock_post.assert_called_once_with("products", data=product_data)
        assert response == response_data

def test_create_variation():
    # Arrange
    service = WCUploadService()
    product_id = 123
    variation_data = {
        "regular_price": "9.99",
        "attributes": [{"name": "Size", "option": "Large"}]
    }
    response_data = {"id": 456, "regular_price": "9.99"}
    
    with patch.object(service.wcapi, 'post', return_value=MagicMock(status_code=201, json=lambda: response_data)) as mock_post:
        # Act
        response = service.create_variation(product_id, variation_data)

        # Assert
        mock_post.assert_called_once_with(f"products/{product_id}/variations", data=variation_data)
        assert response == response_data
