import pytest
from src.pipelines.website_crawling_pipeline import WebsiteCrawlingPipeline
from src.config.ioc import ioc_config
from src.infrastructure.services.bs_crawling_service import BSCrawlingWebService

class TestBSCrawlingWebService(BSCrawlingWebService):
    """
    A test class for crawling web pages and extracting a limited number of URLs.
    """

    def crawling_web(self) -> list:
        """
        Crawl web pages starting from the initial URL and collect up to 10 URLs that match the criteria.

        Returns:
            list: A list of collected URLs.
        """
        print(f'Getting URLs from {self.prefix}...\n')
        logger.info(f'Getting URLs from {self.prefix}...')

        domain = urlparse(self.start_url).netloc
        queue = deque([self.start_url])
        visited = set()
        urls = []
        processed_count = 0

        while queue and len(urls) < 10:
            url = queue.popleft()
            if url in visited:
                continue

            visited.add(url)
            processed_count += 1
            try:
                response = requests.get(url)
                response.raise_for_status()
                logger.debug(f"Fetched URL: {url} with status code: {response.status_code}")
            except requests.RequestException as e:
                logger.error(f"Error processing URL {url}: {e}")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')

            for a in soup.find_all('a', href=True):
                href = a.get('href')
                full_url = urljoin(self.start_url, href)
                logger.debug(f"Extracted href: {href}, Full URL: {full_url}")
                if self.url_validator(full_url, domain, self.prefix) and full_url not in visited:
                    queue.append(full_url)
                    urls.append(full_url)
                    logger.debug(f"Added URL: {full_url}")

            if processed_count % 500 == 0:
                print(f'-{processed_count} URLs processed.')
                logger.info(f'{processed_count} URLs processed.')

        logger.info(f"Crawling finished. Total URLs collected: {len(urls)}")
        return urls

# Prueba unitaria
@pytest.fixture
def setup_container():
    container = ioc_config()
    container.register('crawling_web_service', TestBSCrawlingWebService())
    return container

def test_run_with_real_services(setup_container):
    # Arrange
    pipeline = WebsiteCrawlingPipeline(setup_container)

    # Act
    print("Running pipeline...")
    pipeline.run()
    print("Pipeline run complete.")

    assert True
