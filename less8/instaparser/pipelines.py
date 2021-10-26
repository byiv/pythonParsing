# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.instagramm

    def process_item(self, item, spider):
        print()
        collection = self.mongo_base[item['main_username']]
        collection.insert_one(item)
        return item


class InstaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['user_photo']:
            try:
                yield scrapy.Request(item['user_photo'])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        item['user_photo'] = results[0][1]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = item['user_id']
        dir_name = item['main_username'] + '/' + item['type_friend']
        return f'full/{dir_name}/{image_guid}.jpg'
