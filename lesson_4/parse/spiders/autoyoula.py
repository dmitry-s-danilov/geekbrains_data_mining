import scrapy
# from parse.lib.autoyoula_css import crawl_template, item_template
from parse.lib.autoyoula_xpath import crawl_template, item_template


class AutoYoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.crawl_template = {
            _: crawl_template[_]
            for _ in
            [
                'brands',
                'adverts',
                'adverts_pagination',
            ]
        }

        self.item_template = {
            _: item_template[_]
            for _ in
            [
                'title',
                'description',
                'specification',
                'image_urls',
                'user_url',
                'advert_url',
            ]
        }

        self.database_type = 'MONGO'

    def parse(self, response, **kwargs):
        for _ in self.crawl_template['brands'](response):
            yield response.follow(_.attrib['href'],
                                  callback=self.parse_adverts)

    def parse_adverts(self, response):
        for _ in crawl_template['adverts_pagination'](response):
            yield response.follow(_.attrib['href'],
                                  callback=self.parse_adverts)

        for _ in crawl_template['adverts'](response):
            yield response.follow(_.attrib['href'],
                                  callback=self.parse_advert)

    def parse_advert(self, response):
        yield {
            key: value(response)
            for key, value in
            self.item_template.items()
        }
