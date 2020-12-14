"""
Item pipelines definition.
Each pipeline is to be added to the ITEM_PIPELINES setting.
"""

# Useful for handling different item types with a single interface.
# from itemadapter import ItemAdapter

from os import getenv
from pymongo import MongoClient


class ParsePipeline:
    def __init__(self):
        # client = MongoClient(getenv('DATABASE_CLIENT'))
        # self.database = client[getenv('DATABASE_NAME')]
        self.database = \
            MongoClient(getenv('DATABASE_CLIENT'))[getenv('DATABASE_NAME')]

    def process_item(self, item, spider):
        # collection = self.database[spider.name]
        # collection.insert_one(item)
        self.database[spider.name].insert_one(item)
        return item
