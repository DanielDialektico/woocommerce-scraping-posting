import requests
from bs4 import BeautifulSoup
import json
from src.domain.abstractions import BSScrapingServiceProtocol

class BSScrapingService(BSScrapingServiceProtocol):
    def __init__(self):
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self, url):
        self.response = requests.get(url, headers=self.HEADERS)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        
        tags, product_data = self.scrape_data_tags()
        
        data = {
            "title": self.scrape_title(),
            "price": self.scrape_price(),
            "brand": self.scrape_brand(),
            "description": self.scrape_description(),
            "tags": tags,
            "product_data": product_data,
            "attribute": self.scrape_attribute(),
            "images": self.scrape_images()
        }
        
        return data

    def scrape_title(self):
        """
        Scrape the product title from the web page.

        Returns:
            str: The product title.
        """
        title_selector = '#shopify-section-static-product > section > article > div.product-main > div.product-details > h1'
        title_element = self.soup.select_one(title_selector)
        if title_element:
            return title_element.text.strip()
        return ""

    def scrape_price(self):
        """
        Scrape the product price from the web page.

        Returns:
            str: The product price without currency symbols or commas.
        """
        simple_price_selector = 'div.full_block_nb.medic_price.price--compare-at > div.money'
        price_element = self.soup.select_one(simple_price_selector)
        if price_element:
            return price_element.text.strip().replace('$', '').replace(',', '')
        return ""
    
    def scrape_brand(self):
        """
        Scrape the product brand from the web page.

        Returns:
            str: The product brand.
        """
        brand_selector = '#shopify-section-static-product > section > article > div.product-main > div.product-details > div.product-vendor > a'
        brand_element = self.soup.select_one(brand_selector)
        if brand_element:
            return brand_element['title']
        return ""
    
    def scrape_description(self):
        """
        Scrape the product description from the web page.

        Returns:
            str: The product description.
        """
        description_selector = '#shopify-section-static-product > section > article > div.product-description.rte'
        description_element = self.soup.select_one(description_selector)
        if description_element:
            return description_element.text.strip()
        return ""
    
    def scrape_data_tags(self):
        """
        Scrape the product tags and data from the web page.

        Returns:
            tuple: A tuple containing the product tags (list) and product data (dict).
        """
        script_tag = self.soup.find("script", {"data-section-type": "static-product"})
        product_data = json.loads(script_tag.string)
        tags = product_data["product"]["tags"]
        return tags, product_data
    
    def scrape_attribute(self):
        """
        Scrape the product attribute name from the web page.

        Returns:
            str: The product attribute name.

        Raises:
            ValueError: If the attribute name cannot be found.
        """
        label_tag = self.soup.find("label", {"class": "form-field-title"})
        attribute_name = label_tag.text.strip() if label_tag else None
        if attribute_name is None:
            raise ValueError("No se pudo encontrar el nombre del atributo dinámicamente en la página.")
        return attribute_name
    
    def scrape_images(self):
        """
        Scrape the product images from the web page.

        Returns:
            list: A list of image elements.
        """
        imgs = self.soup.find_all('img', {'data-rimg': 'lazy'})
        return imgs