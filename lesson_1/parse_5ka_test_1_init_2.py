from parse import Parser

parser_specs = [
    {
        'start_url': 'https://5ka.ru/api/regions/'
    },
    {
        'start_url': 'https://5ka.ru/api/v2/categories/',
        'out_dir': 'categories'
    },
    {
        'start_url': 'https://5ka.ru/api/v2/special_offers/',
        'out_dir': 'special_offers',
        'get_delay': .5,
        'run_delay': .25
    }
]

parsers = [Parser(**spec) for spec in parser_specs]

for i, parser in enumerate(parsers, 1):
    print(f'{i}\n{parser}',
          end='\n\n')
