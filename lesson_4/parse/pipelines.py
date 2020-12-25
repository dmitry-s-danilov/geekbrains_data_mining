from os import getenv
from pymongo import MongoClient


class ParsePipeline:
    def __init__(self):
        self.database = \
            MongoClient(getenv('MONGO_CLIENT'))[getenv('MONGO_DATABASE')]

    def process_item(self, item, spider):
        if spider.database_type == 'MONGO':
            self.database[spider.name].insert_one(item)
        return item
