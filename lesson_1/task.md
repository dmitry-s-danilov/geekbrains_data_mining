# Урок 1. Основы клиент-серверного взаимодействия. Парсинг API

## Практическое задание

Организовать сбор данных и сохранение их в `.json` файлы.

Постановка задачи:
- Для каждой категории товаров должен быть создан отдельный файл,
  содержащий товары исключительно данной категории
- При вызове метода/функции сохранения
  скачанные данные записываются в `.json` файлы
- Источники данных:
    - категории: https://5ka.ru/api/v2/categories/
    - товары: https://5ka.ru/special_offers/

Пример структуры данных для файла:
```json
{
  "parent_group_code": "443",
  "parent_group_name": "Алкоголь",
  "producs": [
    {
      "id": 481,
      "name": "Хлебцы Croisette тонкие ржано-пшеничные с прованскими травами 200гр",
      "mech": null,
      "img_link": "https://media.5ka.ru/media/products/4054468.jpg",
      "plu": 4054468,
      "promo": {
        "id": 1146517248,
        "date_begin": "2020-11-17",
        "date_end": "2020-11-23",
        "type": "",
        "description": "",
        "kind": "Z001",
        "expired_at": 5
      },
      "current_prices": {
        "price_reg__min": 134.99,
        "price_promo__min": 87.99
      },
      "store_name": null
    },
    {
      "id": 481,
      "name": "Хлебцы Croisette тонкие ржано-пшеничные с прованскими травами 200гр",
      "mech": null,
      "img_link": "https://media.5ka.ru/media/products/4054468.jpg",
      "plu": 4054468,
      "promo": {
        "id": 1146517248,
        "date_begin": "2020-11-17",
        "date_end": "2020-11-23",
        "type": "",
        "description": "",
        "kind": "Z001",
        "expired_at": 5
      },
      "current_prices": {
        "price_reg__min": 134.99,
        "price_promo__min": 87.99
      },
      "store_name": null
    }
  ]
}
```