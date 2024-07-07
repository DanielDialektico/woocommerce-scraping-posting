import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from src.config.config import CRAWL_URL, CATEGORIES_URL, LOGGING_CRAWLING_FILE
from src.common.utils import setup_logging
from src.domain.abstractions import BSCrawlingWebServiceProtocol

logger = setup_logging(LOGGING_CRAWLING_FILE)

class BSCrawlingWebService(BSCrawlingWebServiceProtocol):
    """
    A service class for crawling web pages and extracting URLs that match certain criteria.
    """

    def __init__(self):
        """
        Initialize the BSCrawlingWebService with the starting URL and URL prefix.
        """
        self.start_url = CRAWL_URL
        self.prefix = CATEGORIES_URL

    def url_validator(self, url: str, domain: str, prefix: str) -> bool:
        """
        Validate if a URL belongs to the same domain and has the desired prefix.

        Args:
            url (str): The URL to validate.
            domain (str): The domain to match.
            prefix (str): The prefix to match.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        is_valid = urlparse(url).netloc == domain and url.startswith(prefix)
        logger.debug(f"URL Validation - URL: {url}, Domain: {domain}, Prefix: {prefix}, Is Valid: {is_valid}")
        return is_valid

    def crawling_web(self) -> list:
        """
        Crawl web pages starting from the initial URL and collect all URLs that match the criteria.

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

        while queue:
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

    def update_prefix(self):
        """
        Update the prefix by removing the last segment.
        """
        self.prefix = '/'.join(self.prefix.rstrip('/').split('/')[:-1]) + '/'