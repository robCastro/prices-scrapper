from django.db import models
from django.contrib.auth.models import User


class Vendor(models.Model):
    TAG_OTHER = "OTHER"
    TAG_META = "META"
    TAG_TYPES = {
        TAG_OTHER: "OTHER",
        TAG_META: "META",
    }
    name = models.CharField(max_length=100)
    selector = models.CharField(max_length=200)
    tag_type = models.CharField(max_length=100, choices=TAG_TYPES, default=TAG_OTHER)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    description = models.CharField(max_length=500)
    url = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.description


class PriceObservation(models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.product}, ${self.price}, {self.created_at:%d/%m/%Y %H:%M:%S}'

