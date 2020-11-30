import os
from pathlib import Path
from parse import ProductParser

if __name__ == '__main__':
    parser = ProductParser(
        start_url='https://5ka.ru/api/v2/special_offers/',
        path_to_save=Path(os.path.dirname(__file__)).joinpath('products'))
    parser.run()
