import os
import requests
import bs4
import pymongo
import dotenv
from time import sleep
from urllib.parse import urljoin

dotenv.load_dotenv('.env')


class Parser:
    _headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'
    }

    _delays = {'get': .5}

    _tags = {
        'catalog': {'name': 'div', 'attrs': {'class': 'сatalogue__main'}},
        # 'data': {'name': 'a', 'class': ['card-sale', 'card-sale_catalogue']},
        'data': {'name': 'a'},

        'header': {'name': 'div', 'attrs': {'class': "card-sale__header"}},
        'title': {'name': 'div', 'attrs': {'class': "card-sale__title"}},

        # 'image_url': {'name': 'img', 'class': 'lazy'},
        'image_url': {'name': 'img'},

        'price_new': {'name': 'div', 'attrs': {'class': 'label__price_new'}},
        'price_old': {'name': 'div', 'attrs': {'class': 'label__price_old'}},
        'price_integer': {
            'name': 'span',
            'attrs': {'class': 'label__price-integer'}
        },
        'price_decimal': {
            'name': 'span',
            'attrs': {'class': 'label__price-decimal'}
        },

        'discount': {'name': 'div', 'attrs': {'class': 'card-sale__discount'}},

        'dates': {'name': 'div', 'attrs': {'class': 'card-sale__date'}},
        'date': {'name': 'p'}
    }

    _data_template = {
        'url':
            lambda soup:
            # soup.attrs['href']
            soup['href'],

        'header':
            lambda soup:
            soup.find(**Parser._tags['header']).findChild().text,

        'title':
            lambda soup:
            soup.find(**Parser._tags['title']).findChild().text,

        'image_url':
            lambda soup:
            # soup.find(**Parser._tags['image_url']).attrs['data-src'],
            soup.find(**Parser._tags['image_url'])['data-src'],

        'prices':
            lambda soup: {
                'new': {
                    'integer':
                        soup.
                        find(**Parser._tags['price_new']).
                        findChild(**Parser._tags['price_integer']).
                        text,
                    'decimal':
                        soup.
                        find(**Parser._tags['price_new']).
                        findChild(**Parser._tags['price_decimal']).
                        text,
                },
                'old': {
                    'integer':
                        soup.
                        find(**Parser._tags['price_old']).
                        findChild(**Parser._tags['price_integer']).text,
                    'decimal':
                        soup.
                        find(**Parser._tags['price_old']).
                        findChild(**Parser._tags['price_decimal']).text,
                },
            },

        'discount':
            lambda soup:
            soup.find(**Parser._tags['discount']).text,

        'dates':
            lambda soup: [
                _.text
                for _ in
                soup.
                find(**Parser._tags['dates']).
                findChildren(**Parser._tags['date'])
            ],
    }

    _dictionary = {
        'с': 'from',
        'до': 'to',

        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12,
    }

    _convert_template = {
        'prices': lambda prices: {
            key: float('.'.join((value['integer'].strip(),
                                 value['decimal'].strip())))
            for key, value in
            prices.items()
        },

        'discount': lambda discount: int(discount.strip()[1:-1]),

        'dates': lambda dates: {
            Parser._translate(preposition): {
                'day': int(day),
                'month': Parser._translate(month)
            }
            for preposition, day, month in
            [date.split() for date in dates]
        },
    }

    def __init__(self,
                 start_url: str, params: dict,
                 database: str, collection: str):
        self.start_url = start_url
        self.params = params
        self.database = database
        self.collection = collection

        self._global_url = lambda url: urljoin(base=self.start_url, url=url)

        # .env
        # DATA_BASE=mongodb://user:pass@localhost:27017/dbname

        # client = pymongo.MongoClient(os.getenv('DATA_BASE'))
        # self._db = client[self.database]

        self._db = pymongo.MongoClient(os.getenv('DATA_BASE'))[self.database]

    @staticmethod
    def _get(*args, **kwargs) -> requests.Response:
        while True:
            try:
                response: requests.Response = requests.get(*args, **kwargs)
                if response.status_code != 200:
                    raise Exception
            except Exception:
                sleep(Parser._delays['get'])
            else:
                return response

    @staticmethod
    def _get_soup(*args, **kwargs) -> bs4.BeautifulSoup:

        # response: requests.Response = Parser._get(*args, **kwargs)
        # text: str = response.text
        # soup: bs4.BeautifulSoup = bs4.BeautifulSoup(text, 'lxml')
        # return soup

        return bs4.BeautifulSoup(Parser._get(*args, **kwargs).text, 'lxml')

    @staticmethod
    def _translate(word: str) -> str:
        return Parser._dictionary[word] if word in Parser._dictionary else word

    @staticmethod
    def _get_data(data_soup: bs4.BeautifulSoup,
                  data_template: dict,
                  convert_template: dict) -> dict:

        data = dict()
        for key, value in data_template.items():
            try:
                data[key] = value(data_soup)
            except Exception:
                continue

        for key, value in convert_template.items():
            try:
                data[key] = value(data[key])
            except Exception:
                continue

        return data

    def parse(self, soup: bs4.BeautifulSoup):
        convert_template: dict = self._convert_template.copy()
        convert_template.update(url=self._global_url,
                                image_url=self._global_url)

        catalog_soup: bs4.element.Tag = soup.find(**self._tags['catalog'])
        for data_soup in catalog_soup.findChildren(**self._tags['data']):

            # todo make a banner exception
            if 'card-sale_banner' in data_soup['class']:
                continue

            data: dict = self._get_data(data_soup=data_soup,
                                        data_template=self._data_template,
                                        convert_template=convert_template)
            yield data

    def save(self, data):
        # collection = self._db[self.collection]
        # collection.insert_one(data)

        self._db[self.collection].insert_one(data)

    def run(self):
        soup = self._get_soup(url=self.start_url,
                              params=self.params,
                              headers=self._headers)
        for data in self.parse(soup):
            self.save(data)
