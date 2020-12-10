"""
Scrapy project settings

Settings documentation:
https://docs.scrapy.org/en/latest/topics/settings.html
https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
https://docs.scrapy.org/en/latest/topics/spider-middleware.html
"""

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

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'parse.middlewares.ParseSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'parse.middlewares.ParseDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'parse.pipelines.ParsePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
