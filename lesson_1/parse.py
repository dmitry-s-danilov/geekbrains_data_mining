import os
import json
import requests
from pathlib import Path
from time import sleep


class Parser:
    _headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
    }

    _params = {
        'records_per_page': 50,
    }

    def __init__(self,
                 start_url: str,
                 get_delay: float = .2,
                 run_delay: float = .1,
                 out_dir: str = None):
        self.start_url: str = start_url
        self.get_delay: float = get_delay
        self.run_delay: float = run_delay
        self.out_path: Path = Path(os.path.dirname(__file__))
        if out_dir:
            self.out_path = self.out_path.joinpath(out_dir)

    def __str__(self):
        return '\n'.join(
            [
                f'URL to begin: {self.start_url}',
                f'get time delay: {self.get_delay}',
                f'run time delay: {self.run_delay}',
                f'path to save: {self.out_path}'
            ]
        )

    def get(self, *args, **kwargs) -> requests.Response:
        while True:
            try:
                response: requests.Response = requests.get(*args, **kwargs)
                if response.status_code != 200:
                    response.raise_for_status()
            except requests.exceptions.InvalidURL as error:
                raise SystemExit(error)
            except requests.exceptions.HTTPError as error:
                status_code_class = int(str(error)[0])
                if status_code_class == 4:
                    raise SystemExit(error)
                else:
                    sleep(self.get_delay)
            # except requests.exceptions.ConnectionError as error:
            #     SystemExit(error)
            # except requests.exceptions.Timeout as error:
            #     SystemExit(error)
            # except requests.exceptions.TooManyRedirects as error:
            #     SystemExit(error)
            # except requests.exceptions.RequestException as error:
            #     SystemExit(error)
            else:
                return response

    def parse(self, url: str):
        params: dict = self._params
        while url:
            response: requests.Response = \
                self.get(url, params=params, headers=self._headers)
            if params:
                params = {}
            # data: dict = json.loads(response.text)
            data: dict = response.json()
            url: str = data.get('next')
            yield data.get('results')

    def save_to_file(self, product):
        path = self.out_path.joinpath(f"{product.get('id')}.json")
        with open(path, 'w', encoding='utf-8') as file:
            # j_data = json.dumps(product, ensure_ascii=False)
            # file.write(j_data)
            json.dump(product, file, ensure_ascii=False)

    def run(self):
        for products in self.parse(self.start_url):
            for product in products:
                self.save_to_file(product)
            sleep(self.run_delay)
