from bs4 import BeautifulSoup
from urllib.request import urlopen

class Producto:
    descripcion: str
    url: str
    selector: str

    def __init__(self, descripcion: str, url: str, selector: str):
        self.descripcion = descripcion
        self.url = url
        self.selector = selector


    def get_precio(self):
        html = urlopen(url=self.url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        price = soup.select_one(self.selector).get_text()
        return price
    