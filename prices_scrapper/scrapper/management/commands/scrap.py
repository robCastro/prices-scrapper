from typing import Any, List, Tuple
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth.models import User
from scrapper.models import Product, PriceObservation
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from scrapper.scrappers import HtmlScrapper, JsonScrapper
from scrapper.models import Vendor

class Command(BaseCommand):
    help = 'Scraps based on product id or all products'
    htmlScrapper = HtmlScrapper()
    jsonScrapper = JsonScrapper()

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--products', nargs='+', type=int)

    def handle(self, *args: Any, **options: Any) -> str | None:
        if options['products']:
            self._scrap_specific_products(options['products'])
        else:
            for user in User.objects.all():
                self._scrap_user_products(user)

    def _scrap_specific_products(self, products: list):
        for product_id in products:
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise CommandError(f'Product {product_id} does not exist.')
            self._scrap(product)

    def _scrap_user_products(self, user: User):
        products = Product.objects.filter(user=user)
        results: list[Tuple[PriceObservation, PriceObservation]] = []
        for product in products:
            try:
                results.append(self._scrap(product))
            except Exception:
                continue
        booleans = [observation.price.compare(previous_observation.price) for previous_observation, observation in results]
        if any(booleans):
            self._send_email(results)


    def _scrap(self, product: Product) -> Tuple[PriceObservation, PriceObservation]:
        try:
            if product.vendor.tag_type == Vendor.TAG_JSON:
                price = self.jsonScrapper.get_price(product)
            else:
                price = self.htmlScrapper.get_price(product)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Can't scrap product {product}")
            )
            print(e)
            raise e
        latest_observation = None
        previous_observation = PriceObservation.objects.filter(product=product)
        observation = PriceObservation(price=price, product=product)
        if previous_observation.exists():
            latest_observation = previous_observation.latest('created_at')
        observation.save()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully scrapped product {product}')
        )
        return [latest_observation, observation]

    def _send_email(self, results: List[Tuple[PriceObservation, PriceObservation]]):
        message = "<h2>Productos con cambio de precio:</h2> <ul>"
        new_prices = []
        same_prices = []
        for result in results:
            if result[0].price.compare(result[1].price) != 0:
                new_prices.append(result)
            else:
                same_prices.append(result)

        for previous_observation, observation in new_prices:
            product_msg = f"<li>{previous_observation.product}: {previous_observation.price} -> {observation.price}</li>"
            message += product_msg
        message += '</ul>'

        if same_prices:
            message += "<h2>Y productos sin cambio:</h2> <ul>"
            for previous_observation, observation in same_prices:
                product_msg = f"<li>{previous_observation.product}: {previous_observation.price} -> {observation.price}</li>"
                message += product_msg
            message += '</ul>'

        send_mail(
            subject=f'You have new prices',
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[results[0][0].product.user.email],
            fail_silently=False,
            html_message=message
        )