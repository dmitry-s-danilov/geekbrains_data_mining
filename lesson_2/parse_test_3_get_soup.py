from parse import Parser


def translate(word: str) -> str:
    dictionary = {
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
    return dictionary[word] if word in dictionary else word


data_template = {
    'url': lambda soup: soup['href'],

    'header': lambda soup:
    soup.find('div', attrs={'class': "card-sale__header"}).text,

    'title': lambda soup:
    soup.find('div', attrs={'class': "card-sale__title"}).text,

    'prices': lambda soup: {
        'new': {
            'integer':
                soup.
                find('div', attrs={'class': 'label__price_new'}).
                findChild('span', attrs={'class': 'label__price-integer'}).
                text,
            'decimal':
                soup.
                find('div', attrs={'class': 'label__price_new'}).
                findChild('span', attrs={'class': 'label__price-decimal'}).
                text
        },
        'old': {
            'integer':
                soup.
                find('div', attrs={'class': 'label__price_old'}).
                findChild('span', attrs={'class': 'label__price-integer'}).
                text,
            'decimal':
                soup.
                find('div', attrs={'class': 'label__price_old'}).
                findChild('span', attrs={'class': 'label__price-decimal'}).
                text
        }
    },

    'image_url': lambda soup: soup.find('img')['data-src'],

    'discount': lambda soup:
    soup.find('div', attrs={'class': 'card-sale__discount'}).text,

    'dates': lambda soup: [
        _.text
        for _ in
        soup.
        find('div', attrs={'class': 'card-sale__date'}).
        findChildren('p')
    ]
}

convert_template = {
    'prices': lambda prices: {
        key: float('.'.join((value['integer'], value['decimal'])))
        for key, value in
        prices.items()
    },

    'discount': lambda discount: int(discount[1:-1]),

    'dates': lambda dates: {
        translate(preposition): {'day': int(day), 'month': translate(month)}
        for preposition, day, month in
        [text.split() for text in dates]
    }
}

if __name__ == '__main__':
    parser = Parser(start_url='https://magnit.ru/promo',
                    params={'geo': 'moskva'},
                    database='data_mining',
                    collection='magnit_promo_moscow')

    # soup = parser._get_soup(parser.start_url, parser.params)

    # catalog = soup.find('div', attrs={'class': 'сatalogue__main'})
    # item = catalog.findChild('a', attrs={'class': 'card-sale'})

    # items = catalog.findChildren('a', attrs={'class': 'card-sale'})
    # item = items[0]

    data_soup =\
        parser._get_soup(parser.start_url, parser.params).\
        find('div', attrs={'class': 'сatalogue__main'}).\
        findChild('a', attrs={'class': 'card-sale'})

    data = {
        key: value(data_soup)
        for key, value in
        data_template.items()
    }

    for key, value in convert_template.items():
        data[key] = value(data[key])

    for _ in data.items():
        print('{}: {}'.format(*_))
