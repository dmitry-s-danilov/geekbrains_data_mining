import re


def user_url_template(user_id):
    user_url_prefix = 'https://youla.ru/user/'
    return user_url_prefix + user_id if user_id else None


user_id_script_inclusion = 'window.transitState = decodeURIComponent'
user_id_script_pattern = re.compile(
    r'youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar'
)

queries = {
    'brands':
        ' '.join(
            (
                'div.ColumnItemList_item__32nYI',
                'a.blackLink',
            )
        ),

    'adverts_pagination':
        ' '.join(
            (
                'div.Paginator_block__2XAPy',
                'a.Paginator_button__u1e7D',
            )
        ),

    'adverts':
        ' '.join(
            (
                'div.SerpSnippet_titleWrapper__38bZM',
                'a.SerpSnippet_name__3F7Yu',
            )
        ),

    'advert':
        {
            'title':
                ' '.join(
                    (
                        'div.AdvertCard_advertTitleRow__3bGJ-',
                        'div.AdvertCard_advertTitle__1S1Ak::text',
                    )
                ),

            'description':
                ' '.join(
                    (
                        'div.AdvertCard_descriptionWrap__17EU3',
                        'div.AdvertCard_descriptionInner__KnuRi::text',
                    )
                ),

            'specification':
                {
                    'rows':
                        ' '.join(
                            (
                                'div.AdvertCard_specs__2FEHc',
                                'div.AdvertSpecs_row__ljPcX'
                            )
                        ),
                    'label': 'div.AdvertSpecs_label__2JHnS::text',
                    'data':
                        [
                            'div.AdvertSpecs_data__xK2Qx::text',
                            'div.AdvertSpecs_data__xK2Qx a.blackLink::text'
                        ]
                },

            'user_id_script':
                f'script:contains("{user_id_script_inclusion}")::text',

            'image_urls':
                ' '.join(
                    (
                        'figure.PhotoGallery_photo__36e_r',
                        'img.PhotoGallery_photoImage__2mHGn',
                    )
                ),
        }
}
