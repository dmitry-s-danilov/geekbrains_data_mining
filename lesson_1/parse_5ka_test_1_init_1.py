from parse import Parser

parser_specs = {
    'regions': 'https://5ka.ru/api/regions/',
    'categories': 'https://5ka.ru/api/v2/categories/',
    'special_offers': 'https://5ka.ru/api/v2/special_offers/',
}

parsers = [
    Parser(start_url=start_url, out_dir=out_dir)
    for out_dir, start_url in parser_specs.items()
]

for i, parser in enumerate(parsers, 1):
    print(f'{i}\n{parser}',
          end='\n\n')
