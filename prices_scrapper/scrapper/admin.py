from django.contrib import admin

from .models import Product, PriceObservation

admin.site.register(Product)
admin.site.register(PriceObservation)
