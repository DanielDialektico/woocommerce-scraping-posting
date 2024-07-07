import pytest
from src.config.ioc import IoCContainer

class DummyService:
    pass

def test_register_and_retrieve_service():
    # Arrange
    container = IoCContainer()
    service_name = 'dummy_service'
    dummy_service = DummyService()
    
    # Act
    container.register(service_name, dummy_service)
    retrieved_service = container.config(service_name)
    
    # Assert
    assert retrieved_service is dummy_service

def test_retrieve_nonexistent_service():
    # Arrange
    container = IoCContainer()
    service_name = 'nonexistent_service'
    
    # Act & Assert
    with pytest.raises(ValueError, match=f"Service '{service_name}' not found"):
        container.config(service_name)