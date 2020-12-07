# Урок 4. Парсинг HTML. Scrapy

## Вебинар

### Обновление и установка модулей

Обновление модулей `pip` и `certifi`. 
```bash
python -m pip install --upgrade pip
pip install --upgrade certifi
```

Установка модуля `scrapy`.
```bash
pip install scrapy
```

### Содание и настройка проекта

Создание scrapy-проекта `parse`.
```bash
scrapy startproject parse .
```

Редактирование настроек в файле `/parse/spiders/settings.py`. 
```python
# Scrapy settings for parse project

BOT_NAME = 'parse'

# Whether to enable logging.
# Default: True
# LOG_ENABLED = False

# Minimum level to log.
# Available: CRITICAL, ERROR, WARNING, INFO, DEBUG.
# Default: 'DEBUG'
# LOG_LEVEL = 'CRITICAL'

SPIDER_MODULES = ['parse.spiders']
NEWSPIDER_MODULE = 'parse.spiders'

# The default User-Agent to use when crawling, unless overridden.
# Default: "parse (+https://scrapy.org)"
# Crawl responsibly by identifying yourself
# (and your website) on the user-agent.
USER_AGENT = \
    'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'

# Obey robots.txt rules.
# Default: True
# If enabled, Scrapy will respect robots.txt policies.
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy.
# Default: 16
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website.
# Default: 0
DOWNLOAD_DELAY = 1

# The download delay setting will honor only one of:

# The maximum number of concurrent (i.e. simultaneous) requests
# that will be performed to any single domain.
# Default: 8
# CONCURRENT_REQUESTS_PER_DOMAIN = 16

# The maximum number of concurrent (i.e. simultaneous) requests
# that will be performed to any single IP.
# Default: 0
# If non-zero, the CONCURRENT_REQUESTS_PER_DOMAIN setting is ignored,
# and this one is used instead.
# In other words, concurrency limits will be applied per IP, not per domain.
# CONCURRENT_REQUESTS_PER_IP = 16

# Whether to enable the cookies middleware.
# Default: True
# If disabled, no cookies will be sent to web servers.
# COOKIES_ENABLED = False

# A boolean which specifies if the telnet console will be enabled
# (provided its extension is also enabled).
# Default: True
TELNETCONSOLE_ENABLED = False

# The default headers used for Scrapy HTTP Requests.
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }
```

### Создание паука

Создание из готовых шаблонов
scrapy-паука `autoyoula` для домена `auto.youla.ru`.
```bash
scrapy genspider autoyoula auto.youla.ru
```

## Практическое задание

- Источник: https://auto.youla.ru/
- Обойти все марки авто и зайти на странички объявлений
- Собрать след стуркутру и сохранить в БД Монго
  - Название объявления
  - Список фото объявления (ссылки)
  - Список характеристик
  - Описание объявления
  - Ссылка на автора объявления
  - Дополнительно попробуйте вытащить номер телефона
