from lxml import html
import requests
from pymongo import MongoClient
import re
import datetime


headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'}
client = MongoClient('localhost', 27017)
db = client['news']


def get_mail_news():
    url = 'https://news.mail.ru'
    response = requests.get(url, headers=headers)
    source = html.fromstring(response.text)
    data = []
    links = source.xpath(f"//ul[@class='list list_type_square list_overflow']//a[@class='link link_flex']/@href")
    for link in links:
        data += [url + link]
    return data


def mail_news_parse_article(link):
    response = requests.get(link, headers=headers)
    source = html.fromstring(response.text)
    info = {'link': link}
    info['date'] = source.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
    info['source'] = source.xpath("//a[@class='link color_gray breadcrumbs__link']//text()")[0]
    info['name'] = source.xpath("//h1[@class='hdr__inner']/text()")[0]

    return info


def mail_news_parsing_collection():
    # Парсинг новостей с mail.ru
    links_mail_new = get_mail_news()
    mail_news_data = []
    for link in links_mail_new:
        mail_news_data.append(mail_news_parse_article(link))
    print(mail_news_data)
    collection = db.news_mail_ru
    collection.insert_many(mail_news_data)


def get_lenta_news_list():
    main_url = 'https://lenta.ru/'
    response = requests.get(main_url, headers=headers)
    source = html.fromstring(response.text)

    links = source.xpath('//a[contains(@href, "/news/")]/@href')
    # Подсмотрено у Василия, как отобрать ссылки с новостями
    links = [main_url + x for x in links if re.search('\/\d{4}\/\d{2}\/\d{2}\/', x)]
    return links


def lenta_news_parse_article(link):
    response = requests.get(link, headers=headers)
    source = html.fromstring(response.text)
    info = {'link': link}
    info['date'] = source.xpath("//time[@class='g-date']/@datetime")[0]
    info['source'] = 'lenta.ru'
    info['name'] = source.xpath("//h1[@class='b-topic__title']//text()")[0]
    print(info)
    return info


def lenta_news_parsing_collection():
    links_lenta_news = get_lenta_news_list()
    lenta_news_data = []
    for link in links_lenta_news:
        lenta_news_data.append(lenta_news_parse_article(link))
    collection = db.news_mail_ru
    collection.insert_many(lenta_news_data)


def get_yandex_news_links():
    main_url = 'https://yandex.ru/news/'
    response = requests.get(main_url, headers=headers)
    source = html.fromstring(response.text)
    news = source.xpath("//a[contains(@href, '/news/story/')]")
    data = []
    for new in news:
        info = {}
        link = new.xpath("./@href")
        info['link'] = main_url[:-6] + link[0]
        grandpa = new.xpath("./../../..")[0]
        text = grandpa.xpath(".//div[contains(@class, 'story__date')]//text()")[0]
        info['title'] = grandpa.xpath('.//h2/a/text()')
        time = text[-5:]
        info['date'] = datetime.datetime.combine(datetime.date.today(),
                                                 datetime.datetime.strptime(time, "%H:%M").time())
        info['source'] = text[:-5]
        data.append(info)
    return data


def yandex_news_parsing_collection():
    yandex_news_data = get_yandex_news_links()
    collection = db.news_mail_ru
    collection.insert_many(yandex_news_data)

# mail_news_parsing_collection()

# lenta_news_parsing_collection()

# yandex_news_parsing_collection()
