# Урок 2. Парсинг HTML. BeautifulSoup. MongoDB

## Практическое задание

### Постановка задачи

- Источник: https://magnit.ru/promo/?geo=moskva
- Необходимо собрать структуры товаров по акции
и сохранить их в MongoDB
- Пример структуры (обязательно хранить поля даты как объекты datetime):
```
{
    "url": str,
    "promo_name": str,
    "product_name": str,
    "old_price": float,
    "new_price": float,
    "image_url": str,
    "date_from": "DATETIME",
    "date_to": "DATETIME",
}
```
