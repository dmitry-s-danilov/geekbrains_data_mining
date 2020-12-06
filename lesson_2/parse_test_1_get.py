import bs4
from parse import Parser

if __name__ == '__main__':
    parser = Parser(start_url='https://magnit.ru/promo',
                    params={'geo': 'moskva'},
                    database='data_mining',
                    collection='magnit_promo_moscow')

    response = parser._get(parser.start_url, parser.params)
    text = response.text
    soup_1 = bs4.BeautifulSoup(text, 'lxml')

    soup_2 = bs4.BeautifulSoup(
        parser._get(parser.start_url, parser.params).text,
        'lxml'
    )

    check = soup_1 == soup_2

    print(check)
