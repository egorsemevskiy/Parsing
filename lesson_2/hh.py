from bs4 import BeautifulSoup as bs
import time
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
            vacancy['price'] = price


            vacancies.append(vacancy)
            print(vacancy)

        else:
            time.sleep(5)
            print('Waiting')


for page in range(1, pages + 1):
    query['page'] = page
    url = create_url(query)
    response = get_html(url)
    soup = bs(response, 'lxml')
    parse_html(soup)
