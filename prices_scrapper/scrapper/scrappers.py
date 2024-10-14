from abc import ABC, abstractmethod
from .models import Product, Vendor
from bs4 import BeautifulSoup, Tag
from decimal import Decimal
from urllib.request import urlopen
from typing import List


class BaseScrapper(ABC):
    @abstractmethod
    def get_price():
        """Scraps the price for a product"""
        pass


class HtmlScrapper(BaseScrapper):
    def _get_price_elements(self, product: Product) -> List[Tag]:
        """
        Gets the price element from the HTML, for example,
        \<strong\>$4,299.99\</strong\> or
        \<meta property="product:price:amount" content="10.74"/\>
        """
        html = urlopen(url=product.url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        price_elements = soup.select(product.vendor.selector)
        if not price_elements:
            raise RuntimeError("No element found for product: " + product)
        return price_elements
    
    def _extract_lowest_price(self, product: Product,  price_elements: Tag) -> Decimal:
        """
        Extracts the price from the html element.
        Currently extracts inner text, or meta tag content.
        """
        prices = []
        if product.vendor.tag_type == Vendor.TAG_META:
            prices = [Decimal(meta['content']) for meta in price_elements]
        elif product.vendor.tag_type == Vendor.TAG_OTHER:
            prices = [Decimal(element.get_text().replace(',', '.').replace('$', '')) for element in price_elements]
        else:
            raise RuntimeError("Vendor tag type not supported for product " + product)
        return min(prices)

    def get_price(self, product: Product) -> Decimal:
        price_elements = self._get_price_elements(product)
        price = self._extract_lowest_price(product, price_elements)
        return price

