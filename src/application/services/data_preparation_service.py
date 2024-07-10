import pandas as pd
from src.common.utils import files_output_path
from src.domain.abstractions import DataPreparationServiceProtocol

class DataPreparationService(DataPreparationServiceProtocol):
    """
    Service for preparing product data for further processing.
    """

    def _convert_attributes(self, row: pd.Series) -> pd.Series:
        """
        Converts product attributes in a DataFrame row.

        Expected input:
        row: pd.Series
        {
            'attribute_name': str,            # Attribute name
            'attribute_options': str,         # Attribute options separated by commas
            'attribute_visible': str,         # Attribute visibility ('True'/'False')
            'attribute_variation': str,       # Whether the attribute is a variation ('True'/'False')
            'default_attributes': str         # Default attributes
        }

        Output:
        row: pd.Series
        {
            'attribute_name': str,            # Attribute name
            'attribute_options': str,         # Attribute options separated by commas
            'attribute_visible': str,         # Attribute visibility ('True'/'False')
            'attribute_variation': str,       # Whether the attribute is a variation ('True'/'False')
            'default_attributes': list[dict], # List of dictionaries with default attributes
            'attributes': list[dict]          # List of dictionaries with attributes
        }
        """
        attributes = []
        if row['attribute_name']:
            attribute = {
                'name': row['attribute_name'],
                'options': row['attribute_options'].split(', ') if row['attribute_options'] else [],
                'visible': bool(row['attribute_visible']),
                'variation': True
            }
            attributes.append(attribute)
        row['attributes'] = attributes

        # Convert default attributes
        default_attributes = []
        if row['default_attributes']:
            default_attribute = {
                'name': row['attribute_name'],
                'option': row['default_attributes']
            }
            default_attributes.append(default_attribute)
        row['default_attributes'] = default_attributes
        return row
    
    def prepare_data(self, products_csv_name: str, descriptions_csv_name) -> pd.DataFrame:
        """
        Prepares data from a CSV file for processing.

        Args:
            csv_name (str): Name of the CSV file to load.

        Returns:
            pd.DataFrame: DataFrame with prepared data.
        """
        csv_path = files_output_path('files\\tables', products_csv_name)
        # Load the CSV file into a DataFrame
        prod_df = pd.read_csv(csv_path, encoding='utf-8')

        desc_csv_path = files_output_path('files\\tables', descriptions_csv_name)
        # Load the CSV file into a DataFrame
        desc_df = pd.read_csv(desc_csv_path, encoding='utf-8')

        # Concat products dataframe with the descriptions dataframe
        df = pd.concat([prod_df, desc_df], axis=1)
        cols = list(df.columns)
        description_column_index = len(cols) - 1
        desired_position = 8
        cols.insert(desired_position, cols.pop(description_column_index))

        df = df[cols]

        # Fill null values with empty strings
        df = df.fillna('')

        # Rename columns
        df = df.rename(columns={
            'attributes': 'attribute_name', 
            'attributes.1': 'attribute_options', 
            'default_attributes': 'default_attributes', 
            'attributes.2': 'attribute_visible', 
            'attributes.3': 'attribute_variation'
        })
        
        # Apply conversion to each row of the DataFrame
        df = df.apply(self._convert_attributes, axis=1)

        # Convert the rows of the DataFrame to a list of dictionaries
        products = df.to_dict(orient='records')

        return products

    def process_images(self, image_urls: str) -> list:
        """
        Processes a string of image URLs into a list of dictionaries.

        Args:
            image_urls (str): Comma-separated string of image URLs.

        Returns:
            list: List of dictionaries, each containing an image URL.
        """
        images = [{'src': url.strip()} for url in image_urls.split(',')] if image_urls else []
        return images