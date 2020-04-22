from bs4 import BeautifulSoup as bs
import time
import urllib.request

vacancy = str(input("Введите название вакансии: "))
pages = int(input("Введите число страниц: "))


headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'}

domain = 'https://www.superjob.ru/'
path = 'vacancy/search/?'
query = {'keywords': vacancy,
         'geo[t][0]': '4',
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
    bodies = html.find_all({'div'}, {'class': 'iJCa5'})

    for b in bodies:
        vacancy = {}

        www = 'https://www.superjob.ru/'
        link_wrapper = b.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})

        if link_wrapper:
            link = link_wrapper.find('a').get('href')
            link = www + link
            title = link_wrapper.text
            price = b.find('span', {'class': 'f-test-text-company-item-salary'}).text

            vacancy['link'] = link
            vacancy['title'] = title
            vacancy['price'] = price
            vacancy['domain'] = domain

            vacancies.append(vacancy)
            print(vacancy)
        else:
            # Тут часто зависает на этом сайте. Не понял еще как сделать ожидание загрузки
            # Динамического контента.
            time.sleep(5)
            print('Waiting')


for page in range(1, pages + 1):
    query['page'] = page
    url = create_url(query)
    response = get_html(url)
    soup = bs(response, 'lxml')
    parse_html(soup)
