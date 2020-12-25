from parse import Parser

if __name__ == '__main__':
    parser = Parser(start_url='https://magnit.ru/promo',
                    params={'geo': 'moskva'},
                    database='data_mining',
                    collection='magnit_promo_moscow')
    parser.run()
