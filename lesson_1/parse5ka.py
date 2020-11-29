import os
from pathlib import Path
import time
import json
import requests


class Parse5ka:
    _headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
    }

    _params = {
        'records_per_page': 50,
    }

    def __init__(self, start_url):
        self.start_url = start_url

    @staticmethod
    def _get(*args, **kwargs) -> requests.Response:
        while True:
            try:
                response = requests.get(*args, **kwargs)
                if response.status_code != 200:
                    # todo create exception class to process status codes
                    raise Exception
                return response
            except Exception:
                time.sleep(.25)

    def parse(self, url):
        # params = Parse5ka._params
        params = self._params
        while url:
            response: requests.Response = \
                self._get(url, params=params, headers=self._headers)
            if params:
                params = {}
            # data: dict = json.loads(response.text)
            data: dict = response.json()
            url = data.get('next')
            yield data.get('results')

    @staticmethod
    def _save_to_file(product):
        path = Path(os.path.dirname(__file__)).\
            joinpath('products').\
            joinpath(f'{product["id"]}.json')
        with open(path, 'w', encoding='utf-8') as file:
            # j_data = json.dumps(product, ensure_ascii=False)
            # file.write(j_data)
            json.dump(product, file, ensure_ascii=False)

    def run(self):
        for products in self.parse(self.start_url):
            for product in products:
                self._save_to_file(product)
            time.sleep(.1)


if __name__ == '__main__':
    parser = Parse5ka(start_url='https://5ka.ru/api/v2/special_offers/')
    parser.run()
