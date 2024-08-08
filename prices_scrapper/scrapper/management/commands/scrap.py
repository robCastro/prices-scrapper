from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from scrapper.models import Product, PriceObservation


class Command(BaseCommand):
    help = 'Scraps based on product id or all products'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--products', nargs='+', type=int)

    def handle(self, *args: Any, **options: Any) -> str | None:
        if options['products']:
            for product_id in options['products']:
                try:
                    product = Product.objects.get(pk=product_id)
                except Product.DoesNotExist:
                    raise CommandError(f'Product {product_id} does not exist.')
                self._scrap(product)
        else:
            for product in Product.objects.all():
                self._scrap(product)

    def _scrap(self, product: Product):
        price = product.get_price()
        PriceObservation.objects.create(price=price, product=product)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully scrapped product {product.id}')
        )