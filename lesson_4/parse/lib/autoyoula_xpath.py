from re import compile
from parse.lib.funcs import find


crawl_queries = {
    'brands':
        '//div[@class="ColumnItemList_item__32nYI"]' +
        '//a[@class="blackLink"]',

    'adverts':
        # '//div[@class="SerpSnippet_titleWrapper__38bZM"]' +
        '//a[contains(@class, "SerpSnippet_name__3F7Yu")]',

    'adverts_pagination':
        # '//div[contains(@class, "Paginator_block__2XAPy")]' +
        '//a[contains(@class, "Paginator_button__u1e7D")]',
}

crawl_template = {
    'brands':
        lambda response:
        response.xpath(crawl_queries['brands']),

    'adverts':
        lambda response:
        response.xpath(crawl_queries['adverts']),

    'adverts_pagination':
        lambda response:
        response.xpath(crawl_queries['adverts_pagination']),
}

user_id_script_text = 'window.transitState = decodeURIComponent'

item_queries = {
    'title':
        # '//div[contains(@class, "AdvertCard_advertTitleRow__3bGJ-")]' +
        '//div[@class="AdvertCard_advertTitle__1S1Ak"]' +
        '/text()',

    'description':
        # '//div[contains(@class, "AdvertCard_descriptionWrap__17EU3")]' +
        '//div[@class="AdvertCard_descriptionInner__KnuRi"]' +
        '/text()',

    'specification':
        {
            'rows':
                # '//div[@class="AdvertCard_specs__2FEHc"]' +
                '//div[@class="AdvertSpecs_row__ljPcX"]',
            'label':
                './div[@class="AdvertSpecs_label__2JHnS"]' +
                '/text()',
            'data':
                [
                    './div[@class="AdvertSpecs_data__xK2Qx"]' +
                    '/text()',
                    './div[@class="AdvertSpecs_data__xK2Qx"]' +
                    '/a[@class="blackLink"]' +
                    '/text()'
                ]
        },

    'image_urls':
        # '//figure[@class="PhotoGallery_photo__36e_r"]' +
        '//img[@class="PhotoGallery_photoImage__2mHGn"]',

    'user_id_script':
        f'//script[contains(text(), "{user_id_script_text}")]' +
        '/text()'
}

user_id_script_pattern = compile(
    r'youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar'
)


def user_url_template(user_id):
    user_url_prefix = 'https://youla.ru/user/'
    return user_url_prefix + user_id if user_id else None


item_template = {
    'advert_url':
        lambda response:
        response.url,

    'title':
        lambda response:
        response.xpath(item_queries['title']).get(),

    'description':
        lambda response:
        response.xpath(item_queries['description']).get(),

    'specification':
        lambda response:
        {
            row.xpath(item_queries['specification']['label']).get():
                row.xpath(item_queries['specification']['data'][0]).get() or
                row.xpath(item_queries['specification']['data'][1]).get()
            for row in
            response.xpath(item_queries['specification']['rows'])
        },

    'image_urls':
        lambda response:
        [
            _.attrib['src']
            for _ in
            response.xpath(item_queries['image_urls'])
        ],

    'user_url':
        lambda response:
        user_url_template(
            find(
                user_id_script_pattern,
                response.xpath(item_queries['user_id_script']).get()
            )
        ),
}
