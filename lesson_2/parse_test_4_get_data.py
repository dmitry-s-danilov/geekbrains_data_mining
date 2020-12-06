import bs4
from parse import Parser


if __name__ == '__main__':
    parser = Parser(start_url='https://magnit.ru/promo',
                    params={'geo': 'moskva'},
                    database='data_mining',
                    collection='magnit_promo_moscow')

    soup: bs4.BeautifulSoup = parser._get_soup(parser.start_url, parser.params)
    catalog_soup: bs4.element.Tag = soup.find(**parser._tags['catalog'])
    data_soup: bs4.element.Tag = catalog_soup.find(**parser._tags['data'])

    data: dict = parser._get_data(data_soup=data_soup,
                                  data_template=parser._data_template,
                                  convert_template=parser._convert_template)

    for _ in data.items():
        print('{}: {}'.format(*_))
