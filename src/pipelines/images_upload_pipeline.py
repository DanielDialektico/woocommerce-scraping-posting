import os
from src.common.utils import setup_logging
from src.config.config import LOGGING_IMAGES_FILE
from src.domain.abstractions import ImagesUploadPipelineProtocol

# Initialize logger
logger = setup_logging(LOGGING_IMAGES_FILE)

class ImagesUploadPipeline(ImagesUploadPipelineProtocol):
    """
    A pipeline class for uploading images to WordPress and updating the product table.
    """

    def __init__(self, container):
        """
        Initialize the ImagesUploadPipeline with the given container.

        Args:
            container (object): The dependency injection container.
        """
        self.container = container
        self.images_factory_service = container.config('images_factory_service')
        self.wp_images_service = container.config('wp_images_service')

    def run(self):
        """
        Run the image upload pipeline.

        Expected input:
        - None

        Expected output:
        - None (uploads images and updates the product table).
        """
        print("\n\n-----Wordpress Images upload Stage-----\n")
        logger.info('Starting Wordpress Images upload Stage')

        print('Preparing data...')
        logger.info('Preparing data...')
        try:
            paths_df = self.images_factory_service.create_paths_table()
            print('Data prepared.')
            logger.info('Data prepared.')
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return
        
        print('\nUploading images...')
        logger.info('Uploading images...')

        counter = 0
        image_urls = []
        for index, row in paths_df.iterrows():
            image_path = row['route']
            try:
                image_url = self.wp_images_service.upload_image(image_path)
                image_urls.append((index, image_url))
                logger.info(f'{image_url}')
            except Exception as e:
                print(f'Error uploading {image_path}: {e}')
                logger.error(f'Error uploading {image_path}: {e}')
                image_urls.append((index, None))
            
            counter += 1

            if counter % 50 == 0:
                print(f'\n{counter} images uploaded.')
                logger.info(f'{counter} images uploaded.')

        try:
            updated_csv = self.images_factory_service.update_wc_table(paths_df, image_urls)
            self.images_factory_service.save_updated_csv(updated_csv)
        except Exception as e:
            logger.error(f"Error updating CSV: {e}")
            print(f"Error updating CSV: {e}")
            return

        print(f'\n{counter} images have been successfully uploaded')
        logger.info(f'{counter} images have been successfully uploaded')