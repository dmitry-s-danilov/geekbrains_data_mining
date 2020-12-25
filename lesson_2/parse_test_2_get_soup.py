import bs4
from parse import Parser

if __name__ == '__main__':
    parser = Parser(start_url='https://magnit.ru/promo',
                    params={'geo': 'moskva'},
                    database='data_mining',
                    collection='magnit_promo_moscow')

    soup = parser._get_soup(parser.start_url, parser.params)

    catalog_1 = soup.find('div', attrs={'class': 'сatalogue__main'})
    catalog_2 = soup.find(
        name='div',
        attrs={'class': {'сatalogue__main', 'js-promo-container'}}
    )

    items_1 = soup.find_all('a', attrs={'class': 'card-sale'})
    items_2 = soup.find_all(
        name='a',
        attrs={'class': {'card-sale', 'card-sale_сatalogue'}}
    )

    items_3 = catalog_1.find_all('a', recursive=False)
    items_4 = catalog_1.find_all(
        name='a',
        attrs={'class': 'card-sale'},
        recursive=False)

    items_5 = catalog_1.findChildren('a')
    items_6 = catalog_1.findChildren(name='a',
                                     attrs={'class': 'card-sale'})

    item_1 = catalog_1.findChild('a')
    item_2 = catalog_1.findChild(name='a',
                                 attrs={'class': 'card-sale'})

    item_3 = items_1[0]
    catalog_3 = item_1.parent

    check = all(
        list(map((lambda _: catalog_1 == _),
                 [catalog_2, catalog_3])) +
        list(map((lambda _: items_1 == _),
                 [items_2, items_3, items_4, items_5, items_6])) +
        list(map((lambda _: item_1 == _),
                 [item_2, item_3]))
    )

    print(check)
