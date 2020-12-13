import os
import scrapy
import pymongo
import dotenv
import re

dotenv.load_dotenv('../../.env')


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    user_id_script_inclusion = 'window.transitState = decodeURIComponent'
    user_id_script_regex = re.compile(
        r'youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar'
    )
    user_url_prefix = 'https://youla.ru/user/'

    def get_user_id(self, script):
        result = re.findall(self.user_id_script_regex, script)
        return result[0] if result else None

    def get_user_url(self, user_id):
        return f'{self.user_url_prefix}{user_id}' if user_id else None

    queries = {
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

            'specification': {
                'rows': ' '.join(
                    (
                        # 'div.AdvertCard_pageContent__24SCy.app_pageBlock__19Uub.app_roundedBlockWithShadow__1rh6w',
                        # 'div.AdvertCard_info__3IKjT AdvertCard_advertBlock__1zrsL',
                        'div.AdvertCard_specs__2FEHc',
                        'div.AdvertSpecs_row__ljPcX'
                    )
                ),
                'label': 'div.AdvertSpecs_label__2JHnS::text',
                'data': [
                    'div.AdvertSpecs_data__xK2Qx::text',
                    'div.AdvertSpecs_data__xK2Qx a.blackLink::text'
                ]
            },

            'user_id_script':
                f'script:contains("{user_id_script_inclusion}")::text',

            'image_urls': ' '.join(
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

    def get_advert_data(self, response):
        queries = AutoyoulaSpider.queries['advert']
        template = {
            'title':
                # response.css(css_query['title'].extract()[0],
                response.css(queries['title']).get(),

            'description':
                response.css(queries['description']).get(),

            'specification': {
                row.css(queries['specification']['label']).get():
                    row.css(queries['specification']['data'][0]).get() or
                    row.css(queries['specification']['data'][1]).get()
                for row in
                response.css(queries['specification']['rows'])
            },

            'advert_url': response.url,

            'user_url':
                self.get_user_url(
                    self.get_user_id(
                        response.css(queries['user_id_script']).get()
                    )
                ),

            'image_urls':
                [_.attrib['src'] for _ in response.css(queries['image_urls'])],
        }
        return template

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.collection = \
            pymongo.MongoClient(
                os.getenv('DATABASE')
            )['data_mining'][self.name]

    def parse(self, response, **kwargs):
        for _ in response.css(self.queries['brands']):
            yield response.follow(_.attrib['href'],
                                  callback=self.parse_adverts)

    def parse_adverts(self, response):
        for _ in response.css(self.queries['adverts_pagination']):
            yield response.follow(_.attrib['href'],
                                  callback=self.parse_adverts)

        for _ in response.css(self.queries['adverts']):
            yield response.follow(_.attrib['href'],
                                  callback=self.parse_advert)

    def parse_advert(self, response):
        data = self.get_advert_data(response)
        self.collection.insert_one(data)
