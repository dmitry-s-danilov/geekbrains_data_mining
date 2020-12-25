import json
import requests
from pathlib import Path
from time import sleep


class Parser:
    _headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'
    }
    _params = {}
    _delays = {'get': .2}

    @staticmethod
    def _get(*args, **kwargs) -> requests.Response:
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
                    sleep(Parser._delays['get'])
            else:
                return response

    @staticmethod
    def _save_to_file(data, path: Path):
        with open(path, 'w', encoding='utf-8') as file:
            # json_data = json.dumps(data, ensure_ascii=False)
            # file.write(json_data)
            json.dump(data, file, ensure_ascii=False)


class ProductParser(Parser):
    _params = {'records_per_page': 50}
    _delays = {'get': .2, 'run': .1}

    def __init__(self, start_url: str, path_to_save: Path):
        self.urls = {'start': start_url}
        self.paths = {'save': path_to_save}

    def _full_path(self, file_name) -> Path:
        return self.paths['save'].joinpath(f'{file_name}.json')

    @staticmethod
    def parse(url: str):
        params: dict = ProductParser._params
        while url:
            response: requests.Response = ProductParser._get(
                url,
                headers=ProductParser._headers,
                params=params
            )
            if params:
                params = {}
            # data: dict = json.loads(response.text)
            data: dict = response.json()
            url: str = data['next']
            yield data['results']

    def run(self):
        for products in self.parse(self.urls['start']):
            for product in products:
                self._save_to_file(product, self._full_path(product['id']))
            sleep(self._delays['run'])


class CatalogParser(ProductParser):
    def __init__(self,
                 start_url: str, catalog_url: str,
                 path_to_save: Path):
        super().__init__(start_url, path_to_save)
        self.urls['catalog'] = catalog_url

    @property
    def categories(self):
        response: requests.Response = self._get(self.urls['catalog'],
                                                params=self._params,
                                                headers=self._headers)
        return response.json()

    def run(self):
        for category in self.categories:
            data = {
                'code': category['parent_group_code'],
                'name': category['parent_group_name'],
                'products': []
            }

            self._params['categories'] = category['parent_group_code']

            for products in self.parse(self.urls['start']):
                data['products'].extend(products)

            self._save_to_file(data,
                               self._full_path(category['parent_group_code']))

            sleep(self._delays['run'])
