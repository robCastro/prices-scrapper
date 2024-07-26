import json
from datetime import datetime
from producto import Producto

def main():
    print('Starting')
    productos = load_products()
    now = datetime.now()
    with open('data.csv', 'a') as file:
        for producto in productos:
            precio = producto.get_precio()
            file.write(f'{producto.descripcion}, {precio}, {now:%d/%m/%Y %H:%M:%S} \n')
    print('Done')

def load_products():
    productos = []
    with open('productos.json', 'r') as file_content:
        json_dictionary = json.load(file_content)
        productos = [Producto(**data) for data in json_dictionary]
    return productos


if __name__ == '__main__':
    main()
