import os
from pathlib import Path
from parse import CatalogParser

if __name__ == '__main__':
    parser = CatalogParser(
        start_url='https://5ka.ru/api/v2/special_offers/',
        catalog_url='https://5ka.ru/api/v2/categories/',
        path_to_save=Path(os.path.dirname(__file__)).joinpath('catalog'))
    parser.run()
