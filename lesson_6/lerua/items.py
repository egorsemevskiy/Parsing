# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose
import re


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def price_item(values):
    values = values.split(' ')
    values = int(''.join(values))
    return values


def name_params_item(values):
    return values


def value_params_item(values):
    values = values.split('\n')
    values = ''.join(values)
    values = re.sub('\s{2,}', '', values)
    return values


class LeruaItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_item), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    name_params = scrapy.Field(input_processor=MapCompose(name_params_item))
    value_params = scrapy.Field(input_processor=MapCompose(value_params_item))
