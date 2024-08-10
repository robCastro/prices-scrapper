from django.db import models
from bs4 import BeautifulSoup
from urllib.request import urlopen
from decimal import Decimal
from django.contrib.auth.models import User


class Product(models.Model):
    description = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
    selector = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.description
    
    def get_price(self) -> Decimal:
        html = urlopen(url=self.url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        price_string = soup.select_one(self.selector).get_text().replace(',', '.').replace('$', '')
        return Decimal(price_string)


class PriceObservation(models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.product}, ${self.price}, {self.created_at:%d/%m/%Y %H:%M:%S}'

