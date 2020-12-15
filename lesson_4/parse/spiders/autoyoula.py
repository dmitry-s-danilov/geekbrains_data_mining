import scrapy
from parse.lib.autoyoula import queries,\
    user_id_script_pattern, user_url_template
from parse.lib.funcs import decoder


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    database_type = 'MONGO'

    item_template = {
        'title': lambda response:
        response.css(queries['advert']['title']).get(),

        'description': lambda response:
        response.css(queries['advert']['description']).get(),

        'specification': lambda response:
        {
            row.css(queries['advert']['specification']['label']).get():
                row.css(queries['advert']['specification']['data'][0]).get() or
                row.css(queries['advert']['specification']['data'][1]).get()
            for row in
            response.css(queries['advert']['specification']['rows'])
        },

        'advert_url': lambda response: response.url,

        'user_url': lambda response:
            user_url_template(
                decoder(
                    user_id_script_pattern,
                    response.css(queries['advert']['user_id_script']).get()
                )
            ),

        'image_urls': lambda response:
        [
            _.attrib['src']
            for _ in
            response.css(queries['advert']['image_urls'])
        ],
    }

    def parse(self, response, **kwargs):
        for _ in response.css(queries['brands']):
            yield response.follow(_.attrib['href'],
                                  callback=self.parse_adverts)

    def parse_adverts(self, response):
        for _ in response.css(queries['adverts_pagination']):
            yield response.follow(_.attrib['href'],
                                  callback=self.parse_adverts)

        for _ in response.css(queries['adverts']):
            yield response.follow(_.attrib['href'],
                                  callback=self.parse_advert)

    def parse_advert(self, response):
        yield {
            key: value(response)
            for key, value
            in self.item_template.items()
        }
