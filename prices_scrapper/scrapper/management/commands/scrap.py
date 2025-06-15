from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from scrapper.models import Product, PriceObservation
from django.core.mail import send_mail
from django.conf import settings
from scrapper.scrappers import HtmlScrapper

class Command(BaseCommand):
    help = 'Scraps based on product id or all products'
    htmlScrapper = HtmlScrapper()

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
        try:
            price = self.htmlScrapper.get_price(product=product)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Can't scrap product {product}")
            )
            print(e)
            return
        previous_observation = PriceObservation.objects.filter(product=product)
        observation = PriceObservation(price=price, product=product)
        if previous_observation.exists():
            latest_observation = previous_observation.latest('created_at')
            if observation.price.compare(latest_observation.price):
                result = f'New price for {product} of {observation.price} before it was {latest_observation.price}'
                print(result)
                self._send_email(product, result)
        observation.save()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully scrapped product {product}')
        )

    def _send_email(self, product: Product, result: str):
        send_mail(
            subject=f'New price for {product}',
            message=result,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[product.user.email],
            fail_silently=False,
        )