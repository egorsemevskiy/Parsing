from bs4 import BeautifulSoup as bs
import time
import numpy as np
import re
from pymongo import MongoClient
import itertools
import urllib.request

vacancy = str(input("Введите название вакансии: "))
pages = int(input("Введите число страниц: "))


headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'}

domain = 'https://spb.hh.ru/'
path = 'search/vacancy/?'
query = {'area': '2',
         'st': 'searchVacancy',
         'text': vacancy,
         'from': 'suggest_post'
         }

vacancies = []

client = MongoClient('localhost', 27017)

def get_html(link):
    try:
        req = urllib.request.Request(url=link, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # with open('test.html', 'w') as output_file:
            #     output_file.write(html)
            return html
    except urllib.request.HTTPError as e:
        if e.code == 404:
            print(f"{link} is not found")
        elif e.code == 503:
            print(f'{link} base webservices are not available')
        else:
            print('http error', e)


def create_url(query):
    params = [f'{k} = {v}' for k, v in query.items()]
    params = '& '.join(params).replace(" ", '')
    url = domain + path + params
    print(url)
    return url


def parse_price(price):
    s_str = '-'
    if price:
        max_price = np.nan
        min_price = np.nan
        currency = price[-4:].replace(' ', '')
        price = price.replace('\xa0', '').replace(' ', '')
        if price[:2] == 'от':
            min_price = int(re.findall('от([\d]*)', price)[0])
        elif price[:2] == 'до':
            max_price = int(re.findall('до([\d]*)', price)[0])
        elif re.findall(s_str, price):
            min_price = int(re.findall('([\d]*)' + s_str, price)[0])
            max_price = int(re.findall(s_str + '([\d]*)', price)[0])
        return min_price, max_price, currency

    return np.nan, np.nan, np.nan


def save_to_mongo(vacancy):
    db = client['vacancies']
    collection = db.vacancies_2020
    collection.insert_one(vacancy)


def parse_html(html):
    bodies = html.find_all({'div'}, {'class': 'vacancy-serp-item'})

    for b in bodies:
        vacancy = {}

        www = 'https://www.hh.ru/'
        link_wrapper = b.find('div', {'class': 'vacancy-serp-item__info'})

        if link_wrapper:
            link = link_wrapper.find('a').get('href')
            title = link_wrapper.find('a').text
            price_wrapper = b.find('div', {'class': 'vacancy-serp-item__sidebar'})
            if price_wrapper:
                price = price_wrapper.find('span')
                if price:
                    price = price.text
                else:
                    price = '000'
            company_wrapper = b.find('div', {'class': 'vacancy-serp-item__meta-info'})
            company = company_wrapper.find('a', {'data-qa': "vacancy-serp__vacancy-employer"}).text
            link = www + link
            vacancy['link'] = link
            vacancy['title'] = title
            vacancy['domain'] = www
            vacancy['company'] = company

            vacancy['min_price'], vacancy['max_price'], vacancy['currency'] = parse_price(price)

            vacancies.append(vacancy)
            print(vacancy)
            save_to_mongo(vacancy)
        else:
            time.sleep(5)
            print('Waiting')


for page in range(1, pages + 1):
    query['page'] = page
    url = create_url(query)
    response = get_html(url)
    soup = bs(response, 'lxml')
    parse_html(soup)
