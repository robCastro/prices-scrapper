from .models import Product, PriceObservation

def scrap_prices():
    print('Starting')
    products = Product.objects.all()
    observations = []
    for product in products:
        price = product.get_price()
        observation = PriceObservation(price=price, product=product)
        observations.append(observation)
    PriceObservation.objects.bulk_create(observations)
    print('Done')
