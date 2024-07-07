import pytest
from unittest.mock import MagicMock, patch
from src.pipelines.images_upload_pipeline import ImagesUploadPipeline

def test_run():
    # Arrange
    container_mock = MagicMock()
    images_factory_service_mock = container_mock.config.return_value
    wp_images_service_mock = container_mock.config.return_value

    paths_df_mock = MagicMock()
    paths_df_mock.iterrows.return_value = iter([(0, {'route': 'path/to/image1.jpg'}), (1, {'route': 'path/to/image2.jpg'})])
    images_factory_service_mock.create_paths_table.return_value = paths_df_mock

    wp_images_service_mock.upload_image.side_effect = ['http://example.com/image1.jpg', 'http://example.com/image2.jpg']
    images_factory_service_mock.update_wc_table.return_value = MagicMock()

    pipeline = ImagesUploadPipeline(container_mock)

    # Act
    with patch('src.pipelines.images_upload_pipeline.logger') as logger_mock:
        pipeline.run()

    # Assert
    images_factory_service_mock.create_paths_table.assert_called_once()
    wp_images_service_mock.upload_image.assert_any_call('path/to/image1.jpg')
    wp_images_service_mock.upload_image.assert_any_call('path/to/image2.jpg')
    images_factory_service_mock.update_wc_table.assert_called_once()
    images_factory_service_mock.save_updated_csv.assert_called_once()
    logger_mock.info.assert_any_call('Starting Wordpress Images upload Stage')
    logger_mock.info.assert_any_call('Data prepared.')
    logger_mock.info.assert_any_call('http://example.com/image1.jpg')
    logger_mock.info.assert_any_call('http://example.com/image2.jpg')
    logger_mock.info.assert_any_call('2 images have been successfully uploaded')