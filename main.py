from datetime import datetime
from repositories import ProductRepository, PriceObservationRepository
from models import PriceObservation
from db import conn

def main():
    print('Starting')
    product_repository = ProductRepository()
    price_repository = PriceObservationRepository()
    now = datetime.now()
    products = product_repository.find_all()
    for product in products:
        price = product.get_price()
        observation = PriceObservation(id=None, price=price, created_at=now, product_id=product.id)
        result = price_analysis(observation, price_repository)
        print(result)
        # price_repository.save(observation)
    conn.close()
    print('Done')

def price_analysis(price_observation: PriceObservation, price_repository: PriceObservationRepository) -> str: 
    result = ''
    latest_price = price_repository.find_latest_by_product_id(price_observation.product_id)
    avg_price = price_repository.find_average_price_by_product_id(price_observation.product_id)    
    if price_observation.price < avg_price:
        result += f'New price for product {price_observation.product_id} of {price_observation.price} is under avg, it was {avg_price}, latest price was {latest_price.price}\n'
    else:
        result += f'New price for product {price_observation.product_id} of {price_observation.price} before it was {latest_price.price} avg is {avg_price}\n'
    return result

if __name__ == '__main__':
    main()
