from parse import Parser

if __name__ == '__main__':
    parser = Parser(start_url='https://5ka.ru/api/v2/special_offers/',
                    out_dir='special_offers')
    parser.run()
