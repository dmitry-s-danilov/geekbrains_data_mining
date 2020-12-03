import requests
import bs4
from time import sleep


class Parser:
    _headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'
    }

    _delays = {'get': .5}

    @staticmethod
    def _get(*args, **kwargs) -> requests.Response:
        while True:
            try:
                response = requests.get(*args, **kwargs)
                if response.status_code != 200:
                    raise Exception
            except Exception:
                sleep(Parser._delays['get'])
            else:
                return response

    @staticmethod
    def _soup(*args, **kwargs) -> bs4.BeautifulSoup:
        # response: requests.Response = Parser._get(*args, **kwargs)
        # text: str = response.text
        # soup: bs4.BeautifulSoup = bs4.BeautifulSoup(text, 'lxml')
        # return soup
        return bs4.BeautifulSoup(Parser._get(*args, **kwargs).text, 'lxml')


class ProductParser(Parser):
    def __init__(self, url_to_start: str, params: dict):
        self._urls = {'start': url_to_start}
        self._params = params

    def run(self):
        soup = self._soup(self._urls['start'],
                          headers=self._headers,
                          params=self._params)
        print(1)


if __name__ == '__main__':
    parser = ProductParser(url_to_start='https://magnit.ru/promo/?geo=moskva',
                           params={})
    parser.run()
