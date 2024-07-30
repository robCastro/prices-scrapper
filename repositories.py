from models import Product, PriceObservation
from typing import List
from sqlite3 import Cursor
from db import conn

class ProductRepository:
    __cursor: Cursor

    def __init__(self) -> None:
        self.__cursor = conn.cursor()
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS PRODUCT(
            id integer primary key autoincrement,
            description text,
            url text,
            selector text
        )
        """)

    def find_all(self) -> List[Product]:
        self.__cursor.execute('SELECT * FROM PRODUCT') 
        products_list = self.__cursor.fetchall()
        return [Product(*data_tuple) for data_tuple in products_list]

    def find_by_id(self, id: int) -> Product:
        self.__cursor.execute('SELECT * FROM PRODUCT WHERE id = ?', (id,))
        product_dict = self.__cursor.fetchone()
        return Product(**product_dict)

    def save(self, product: Product) -> None:
        retorno = self.__cursor.execute('INSERT INTO PRODUCT (description, url, selector) VALUES (?, ?, ?)', (product.description, product.url, product.selector))
        print(retorno)
        conn.commit()


class PriceObservationRepository:
    __cursor: Cursor

    def __init__(self) -> None:
        self.__cursor = conn.cursor()
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS PRICE_OBSERVATION(
            id integer primary key autoincrement,
            price real,
            created_at text,
            product_id integer,
            FOREIGN KEY(product_id) REFERENCES PRODUCT(id)
        )
        """)

    def find_all(self) -> List[PriceObservation]:
        self.__cursor.execute('SELECT * FROM PRICE_OBSERVATION') 
        prices_list = self.__cursor.fetchall()
        return [PriceObservation(*data_tuple) for data_tuple in prices_list]

    def find_by_id(self, id: int) -> PriceObservation:
        self.__cursor.execute('SELECT * FROM PRICE_OBSERVATION WHERE id = ?', (id,))
        price_dict = self.__cursor.fetchone()
        return PriceObservation(**price_dict)
    
    def find_by_product_id(self, product_id: int) -> List[PriceObservation]:
        self.__cursor.execute('SELECT * FROM PRICE_OBSERVATION WHERE product_id = ?', (product_id,)) 
        prices_list = self.__cursor.fetchall()
        return [PriceObservation(*data_tuple) for data_tuple in prices_list]
    
    def find_latest_by_product_id(self, product_id: int) -> PriceObservation:
        self.__cursor.execute('SELECT * FROM PRICE_OBSERVATION WHERE product_id = ? ORDER BY id DESC LIMIT 1', (product_id,)) 
        price_dict = self.__cursor.fetchone()
        return PriceObservation(*price_dict)
    
    def find_average_price_by_product_id(self, product_id: int) -> float:
        self.__cursor.execute('SELECT AVG(price) FROM PRICE_OBSERVATION WHERE product_id = ?', (product_id,)) 
        avg_price = self.__cursor.fetchone()[0]
        return avg_price

    def save(self, price_observation: PriceObservation) -> None:
        retorno = self.__cursor.execute('INSERT INTO PRICE_OBSERVATION (price, created_at, product_id) VALUES (?, ?, ?)', (price_observation.price, price_observation.created_at, price_observation.product_id))
        print(retorno)
        conn.commit()
