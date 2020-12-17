from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from parse.spiders.autoyoula import AutoYoulaSpider
from dotenv import load_dotenv

load_dotenv('.env')

if __name__ == '__main__':
    settings = Settings()
    settings.setmodule('parse.settings')

    process = CrawlerProcess(settings=settings)
    process.crawl(AutoYoulaSpider)

    process.start()
