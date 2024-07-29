import json
from datetime import datetime
from producto import Producto
from pathlib import Path

def main():
    print('Starting')
    now = datetime.now()
    current_path = Path(__file__).parent
    productos = load_products(current_path)
    filename = current_path.joinpath('data.csv')
    with open(filename, 'a') as file:
        for producto in productos:
            precio = producto.get_precio()
            file.write(f'{producto.descripcion}, {precio}, {now:%d/%m/%Y %H:%M:%S} \n')
    print('Done')

def load_products(current_path: Path):
    productos = []
    filename = current_path.joinpath('productos.json')
    with open(filename, 'r') as file_content:
        json_dictionary = json.load(file_content)
        productos = [Producto(**data) for data in json_dictionary]
    return productos


if __name__ == '__main__':
    main()
