# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = [f'https://www.superjob.ru/vacancy/search/?keywords=Продавец&geo%5Bt%5D%5B0%5D=4&page={idx}' \
                  for idx in range(1, 11)]

    def parse(self, response: HtmlResponse):
        for url in response.xpath(
                '//div[@class="_3mfro CuJz5 PlM3e _2JVkc _3LJqf"]//a[contains(@class, "icMQ_")]/@href'):
            yield response.follow(url, callback=self.sj_vacancy_parse)

    def sj_vacancy_parse(self, response: HtmlResponse):
        item = ItemLoader(JobparserItem(), response)
        item.add_value('url', response.url)
        item.add_xpath('title', '//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]//text()')
        item.add_xpath('price', '//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]//text()')
        # item.add_xpath('tags', '//div[@class="vacancy-section"]//span[@data-qa="bloko-tag__text"]//text()')
        item.add_xpath('organization', \
                       '//div[@class="_1cFsi _3VUIu"]//div[contains(@class, "_3zucV")]//a[contains(@class, "_2JivQ")]//text()')
        item.add_xpath('company_link', \
                       '//div[@class="_1cFsi _3VUIu"]//div[contains(@class, "_3zucV")]//a[contains(@class, "_2JivQ")]//@href')
        yield item.load_item()