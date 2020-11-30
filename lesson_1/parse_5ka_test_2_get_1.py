from parse import Parser

urls = [
    'https://5ka.ru/api/regions/',
    'https://5ka.ru/api/v2/categories/',
    'https://5ka.ru/api/v2/special_offers/'
]

parser = Parser(urls[0])
responses = [parser.get(url) for url in urls]

for i, response in enumerate(responses):
    print(i,
          f'url: {response.url}',
          f'status code: {response.status_code}',
          sep='\n', end='\n\n')
