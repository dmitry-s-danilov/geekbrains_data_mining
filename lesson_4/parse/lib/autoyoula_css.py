from re import compile
from parse.lib.funcs import find


crawl_queries = {
    'brands':
        'div.ColumnItemList_item__32nYI' + ' ' +
        'a.blackLink',

    'adverts':
        # 'div.SerpSnippet_titleWrapper__38bZM' + ' ' +
        'a.SerpSnippet_name__3F7Yu',

    'adverts_pagination':
        # 'div.Paginator_block__2XAPy' + ' ' +
        'a.Paginator_button__u1e7D',
}

crawl_template = {
    'brands':
        lambda response:
        response.css(crawl_queries['brands']),

    'adverts':
        lambda response:
        response.css(crawl_queries['adverts']),

    'adverts_pagination':
        lambda response:
        response.css(crawl_queries['adverts_pagination']),
}

user_id_script_text = 'window.transitState = decodeURIComponent'

item_queries = {
    'title':
        # 'div.AdvertCard_advertTitleRow__3bGJ-' + ' ' +
        'div.AdvertCard_advertTitle__1S1Ak' +
        '::text',

    'description':
        # 'div.AdvertCard_descriptionWrap__17EU3' + ' ' +
        'div.AdvertCard_descriptionInner__KnuRi' +
        '::text',

    'specification':
        {
            'rows':
                # 'div.AdvertCard_specs__2FEHc' + ' ' +
                'div.AdvertSpecs_row__ljPcX',
            'label':
                'div.AdvertSpecs_label__2JHnS' +
                '::text',
            'data':
                [
                    'div.AdvertSpecs_data__xK2Qx' +
                    '::text',
                    'div.AdvertSpecs_data__xK2Qx' + ' ' +
                    'a.blackLink' +
                    '::text'
                ]
        },

    'image_urls':
        # 'figure.PhotoGallery_photo__36e_r' + ' ' +
        'img.PhotoGallery_photoImage__2mHGn',

    'user_id_script':
        f'script:contains("{user_id_script_text}")' +
        '::text',
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
        response.css(item_queries['title']).get(),

    'description':
        lambda response:
        response.css(item_queries['description']).get(),

    'specification':
        lambda response:
        {
            row.css(item_queries['specification']['label']).get():
                row.css(item_queries['specification']['data'][0]).get() or
                row.css(item_queries['specification']['data'][1]).get()
            for row in
            response.css(item_queries['specification']['rows'])
        },

    'image_urls':
        lambda response:
        [
            _.attrib['src']
            for _ in
            response.css(item_queries['image_urls'])
        ],

    'user_url':
        lambda response:
        user_url_template(
            find(
                user_id_script_pattern,
                response.css(item_queries['user_id_script']).get()
            )
        ),
}
