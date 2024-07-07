import pytest
import pandas as pd
from src.config.config import TEST_SCRAPE_URLS
from src.common.utils import files_output_path
from src.pipelines.website_scraping_pipeline import WebsiteScrapingPipeline
from src.config.ioc import ioc_config

@pytest.fixture
def setup_container():
    container = ioc_config()
    return container

def test_run_with_real_services(setup_container):
    
    pipeline = WebsiteScrapingPipeline(setup_container)

    urls_path = files_output_path('files\\tables', TEST_SCRAPE_URLS)

    urls_df = pd.read_csv(urls_path, encoding='latin1')
    urls_to_test = urls_df['Cleaned_URL'] 

    assert len(urls_to_test) > 0, "Test should have some URLs"

    # Act
    print("Running pipeline...")
    pipeline.run()
    print("Pipeline run complete.")

    assert True