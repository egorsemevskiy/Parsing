# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'jobparser'
    allowed_domains = ['hh.ru']

    def __init__(self, text):
        self.start_urls = [
            f'https://izhevsk.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text={text}&showClusters=false']

    def parse(self, response: HtmlResponse):
        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

    def vacancy_parce(self, response: HtmlResponse):
        item = ItemLoader(JobparserItem(), response)
        item.add_value('url', response.url)
        item.add_xpath('title', '//h1[@class="header"]//text()')
        item.add_xpath('price', '//p[@class="vacancy-salary"]//text()')
        item.add_xpath('tags', '//div[@class="vacancy-section"]//span[@data-qa="bloko-tag__text"]//text()')
        item.add_xpath('organization', '//a[@class="vacancy-company-name"]/span[@itemprop="name"]//text()')
        item.add_xpath('company_link', '//a[@class="vacancy-company-name"]/@href')
        item.add_xpath('logo', '//a[@class="vacancy-company-logo"]/img/@src')
        yield item.load_item()




