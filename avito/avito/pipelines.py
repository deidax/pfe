# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import pyfiglet

from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
import logging
from termcolor import colored

class MongoDBPipeline(object):

    collection_name = 'products'
    items_processed_count = 0

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'avito')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        finished_text = 'DONE '+str(self.items_processed_count)+' PRODUCTS INSERTED !'
        finished_text = pyfiglet.figlet_format(finished_text, font = "digital" )
        finished_text = colored(finished_text, 'green', attrs=['bold'])
        print('\n')
        print(finished_text)
        self.client.close()

    def process_item(self, item, spider):
        products_collection = self.db[self.collection_name]
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            product = item.get('product_data_items')
            product_id = product.get('product_id')
            _filter = {}
            for key in ["product_id"]:
                _filter[key] = eval(key)
                
            if _filter:
                try:
                    item_return = item
                    item = item.get('product_data_items')
                    query_result = products_collection.update(_filter, dict(item), upsert=True)
                    self.items_processed_count += 1
                    print(colored(" [MONGODB] OK!: "+str(query_result), 'yellow'))
                    if query_result['updatedExisting']:
                        return print(colored(item_return, 'yellow'))
                    return item_return
                except pymongo.errors.PyMongoError as e:
                    print(colored(" [!][MONGODB-ERROR] DB Not Updated! [ "+e+" ]", 'red'))
                    print(colored("[MONGODB]--> Product Error <--\n", 'red'))
                    print(colored(item_return, 'red'))

                
