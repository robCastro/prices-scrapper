from django.contrib import admin

from .models import Product, PriceObservation, Vendor


class PriceObservationAdmin(admin.ModelAdmin):
    list_filter = ['product', 'product__user', 'created_at']
    list_display = ['product', 'price', 'created_at']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['description', 'user']
    list_filter = ['user', 'vendor']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'tag_type']


admin.site.register(Product, ProductAdmin)
admin.site.register(PriceObservation, PriceObservationAdmin)
admin.site.register(Vendor, VendorAdmin)