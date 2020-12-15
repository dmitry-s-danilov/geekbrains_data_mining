from os import getenv
from pymongo import MongoClient


class ParsePipeline:
    def __init__(self):
        # client = MongoClient(getenv('MONGO_CLIENT'))
        # self.database = client[getenv('MONGO_DATABASE')]
        self.database = \
            MongoClient(getenv('MONGO_CLIENT'))[getenv('MONGO_DATABASE')]

    def process_item(self, item, spider):
        if spider.database_type == 'MONGO':
            # collection = self.database[spider.name]
            # collection.insert_one(item)
            self.database[spider.name].insert_one(item)
        return item
