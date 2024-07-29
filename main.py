from datetime import datetime
from pathlib import Path
from repositories import ProductRepository, PriceObservationRepository
from models import PriceObservation

def main():
    print('Starting')
    product_repository = ProductRepository()
    price_repository = PriceObservationRepository()
    now = datetime.now()
    products = product_repository.find_all()
    for product in products:
        price = product.get_price()
        observation = PriceObservation(id=None, price=price, created_at=now, product_id=product.id)
        price_repository.save(observation)
    print('Done')

if __name__ == '__main__':
    main()
