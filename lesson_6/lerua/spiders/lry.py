# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lerua.items import LeruaItem
from scrapy.loader import ItemLoader


class LrySpider(scrapy.Spider):
    name = 'lry'
    allowed_domains = ['spb.leroymerlin.ru']
    start_urls = ['https://spb.leroymerlin.ru/catalogue/shtukaturki/']

    def parse(self, response: HtmlResponse):
        next_page = response.css("div.next-paginator-button-wrapper a::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        item_links = response.xpath("//a[@class='black-link product-name-inner']/@href").extract()
        for link in item_links:
            yield response.follow(link, callback=self.item_parse)

    def item_parse(self, response: HtmlResponse):
        item = ItemLoader(item=LeruaItem(), response=response)
        item.add_xpath('name', "//h1[@class='header-2']/text()")
        item.add_xpath('price', "//span[@slot='price']/text()")
        item.add_xpath('photos', "//uc-pdp-media-carousel[@slot='media-content']//picture/@srcset")
        item.add_xpath('name_params', "//dt[@class='def-list__term']/text()")
        item.add_xpath('value_params', "//dd[@class='def-list__definition']/text()")
        yield item.load_item()

