# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class LolPipeline(object):

    collection_name = 'lol_rank'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crwaler):
        return cls(
            mongo_uri = crwaler.settings.get('MONGO_URI'),
            mongo_db = crwaler.settings.get('MONGO_DB')            
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        print(item)
        self.db[self.collection_name].insert_one(dict(item))
        return item
