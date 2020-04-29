# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os
from urllib.parse import urlparse


class LeruaPipeline(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lerua_29

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LeruaImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        return f'files/{os.path.basename(urlparse(request.url).path)[:8]}/' + os.path.basename(
            urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results[0]:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
