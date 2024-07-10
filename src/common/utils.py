import os
import logging

def files_output_path(directory: str, filename: str) -> str:
    """
    Ensure the directory exists and return the full path for the output file.

    Args:
        directory (str): The directory where the file will be saved.
        filename (str): The name of the file to be saved.

    Returns:
        str: The full path of the file.
    """
    # Ajustar la lógica para que el directorio raíz sea el directorio del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    output_dir = os.path.join(project_root, directory)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, filename)

def setup_logging(service_name: str):
    """
    Set up logging for a specific service.

    Args:
        service_name (str): The name of the service for logging that is going to create a file to save the logs.
    """
    log_directory = files_output_path('logs', service_name)
    os.makedirs(os.path.dirname(log_directory), exist_ok=True)

    logger = logging.getLogger(service_name)
    if not logger.hasHandlers():
        handler = logging.FileHandler(log_directory)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger