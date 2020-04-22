# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    # TODO преобразовать в список в строку price
    price = scrapy.Field()
    tags = scrapy.Field()
    organization = scrapy.Field()
    logo = scrapy.Field(output_processor=TakeFirst())
    company_link = scrapy.Field(output_process=TakeFirst())


