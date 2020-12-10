from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
# from parse import settings
from parse.spiders.autoyoula import AutoyoulaSpider


if __name__ == '__main__':
    crawl_settings = Settings()
    # crawl_settings.setmodule(settings)
    crawl_settings.setmodule('parse.settings')

    crawl_process = CrawlerProcess(settings=crawl_settings)
    crawl_process.crawl(AutoyoulaSpider)

    crawl_process.start()
