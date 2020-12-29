# Урок 2. Парсинг HTML. BeautifulSoup. PyMongo

## Практическое задание

Требуется собрать данные о товарах по акции и
сохранить их в коллекцию базы данных *MongoDB*.

- Источник данных: https://magnit.ru/promo/?geo=moskva

- Даты должны быть сохранены как объекты *datetime*

- Описание структуры данных одного товара,
  соответствующей отдельной записи
  в коллекции базы данных *MongoDB*:

  ```
  {
      'url': str,
      'promo_name': str,
      'product_name': str,
      'old_price': float,
      'new_price': float,
      'image_url': str,
      'date_from': datetime,
      'date_to': datetime,
  }
  ```
