from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

class Product:
    id: int
    description: str
    url: str
    selector: str

    def __init__(self, id: int, description: str, url: str, selector: str) -> None:
        self.id = id
        self.description = description
        self.url = url
        self.selector = selector


    def get_price(self) -> float:
        html = urlopen(url=self.url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        price_string = soup.select_one(self.selector).get_text().replace(',', '.').replace('$', '')
        return float(price_string)
    
    def __repr__(self) -> str:
        return f'Product: {self.description}'
    

class PriceObservation:
    id: int
    price: float
    created_at: datetime
    product_id: int

    def __init__(self, id: int, price: float, created_at: datetime, product_id: int) -> None:
        self.id = id
        self.price = price
        self.created_at = created_at
        self.product_id = product_id

    def __repr__(self) -> str:
        return f'Price Observation for Product {self.product_id}: {self.price} at {self.created_at}'
    
