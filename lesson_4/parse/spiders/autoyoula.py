import os
import scrapy
import pymongo
import dotenv

dotenv.load_dotenv('../../.env')


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    css_queries = {
        'brands': ' '.join(
            (
                # 'div.TransportMainFilters_brandsList__2tIkv',
                # 'div.ColumnItemList_container__5gTrc',
                # 'div.ColumnItemList_column__5gjdt',
                'div.ColumnItemList_item__32nYI',
                'a.blackLink',
            )
        ),

        'adverts_pagination': ' '.join(
            (
                # 'div.Paginator_block__2XAPy.app_roundedBlockWithShadow__1rh6w',
                'div.Paginator_block__2XAPy',
                # 'a.Paginator_button__u1e7D.ButtonLink_button__1wyWM.Button_button__3NYks',
                'a.Paginator_button__u1e7D',
            )
        ),

        'adverts': ' '.join(
            (
                # 'article.SerpSnippet_snippet__3O1t2.app_roundedBlockWithShadow__1rh6w',
                # 'div.SerpSnippet_snippetContent__d8CHK',
                # 'div.SerpSnippet_data__3ezjY',
                # 'div.SerpSnippet_topInfo__1ZraC',
                'div.SerpSnippet_titleWrapper__38bZM',
                # 'a.SerpSnippet_name__3F7Yu.SerpSnippet_titleText__1Ex8A.blackLink',
                'a.SerpSnippet_name__3F7Yu',
            )
        ),

        'advert': {
            'title': ' '.join(
                (
                    # 'div.AdvertCard_pageContent__24SCy.app_pageBlock__19Uub.app_roundedBlockWithShadow__1rh6w',
                    # 'div.AdvertCard_topAdvertHeader__iqqNl',
                    # 'div.AdvertCard_topAdvertHeaderInfo__OiPAZ',
                    # 'div.AdvertCard_advertTitleRow__3bGJ-.AdvertCard_topAdvertHeaderCommon__2zUjb',
                    'div.AdvertCard_advertTitleRow__3bGJ-',
                    'div.AdvertCard_advertTitle__1S1Ak::text',
                )
            ),

            'description': ' '.join(
                (
                    # 'div.AdvertCard_pageContent__24SCy.app_pageBlock__19Uub.app_roundedBlockWithShadow__1rh6w',
                    # 'div.AdvertCard_description__2bVlR.AdvertCard_advertBlock__1zrsL',
                    'div.AdvertCard_descriptionWrap__17EU3',
                    'div.AdvertCard_descriptionInner__KnuRi::text',
                )
            ),

            'images': ' '.join(
                (
                    # 'div.AdvertCard_pageContent__24SCy.app_pageBlock__19Uub.app_roundedBlockWithShadow__1rh6w',
                    # 'div.AdvertCard_info__3IKjT.AdvertCard_advertBlock__1zrsL',
                    # 'div',
                    # 'div.PhotoGallery_block__1ejQ1',
                    # 'div.PhotoGallery_photoWrapper__3m7yM',
                    'figure.PhotoGallery_photo__36e_r',
                    # 'picture',
                    'img.PhotoGallery_photoImage__2mHGn',
                )
            ),
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.collection = \
            pymongo.MongoClient(
                os.getenv('DATABASE')
            )['data_mining'][self.name]

    @property
    def advert_template(self):
        queries = self.css_queries['advert']
        template = {
            'title':
                lambda response:
                # response.css(css_query['title'].extract()[0],
                response.css(queries['title']).get(),

            'description':
                lambda response:
                response.css(queries['description']).get(),

            # 'specification': lambda response: '',

            'images':
                lambda response:
                [_.attrib['src'] for _ in response.css(queries['images'])],

            # 'author': lambda response: '',

            # 'url': lambda response: '',
        }
        return template

    def parse(self, response, **kwargs):
        for _ in response.css(self.css_queries['brands']):
            yield response.follow(_.attrib['href'],
                                  callback=self.adverts_parse)

    def adverts_parse(self, response):
        for _ in response.css(self.css_queries['adverts_pagination']):
            yield response.follow(_.attrib['href'],
                                  callback=self.adverts_parse)

        for _ in response.css(self.css_queries['adverts']):
            yield response.follow(_.attrib['href'],
                                  callback=self.advert_parse)

    def advert_parse(self, response):
        data = {
            key: value(response)
            for key, value in
            self.advert_template.items()
        }

        self.collection.insert_one(data)
