from bs4 import BeautifulSoup as bs
import requests

text = 'python'
items = 50
headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Yandex',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br'
}
url = 'https://hh.ru/search/vacancy?L_save_area=true&text=python&excluded_text=&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=100&hhtmFrom=vacancy_search_filter'
# def hh():
#     request = requests.get(url, headers=headers)
#     # print(request.status_code)
#     # print(request.text)
#     soup = bs(request.text, 'lxml')
#     paginator = soup.find_all('span', {'class': 'pager-item-not-in-short-range'})
#     pages=[]
#     for page in paginator:
#         pages.append(int(page.find('a').text))
#     if len(pages) == 0:
#         return 1
#     else:
#         return pages[-1]
# max_page = hh()


def get_url():
    request = requests.get(url, headers=headers)
    soup = bs(request.text, 'lxml')
    data = soup.find_all('div',  {'class': 'vacancy-search-item__card'})
    for i in data:
        card_url = i.find('a').get('href')
        yield card_url

def array():
    for card_url in get_url():
        response = requests.get(card_url, headers=headers)
        soup = bs(response.text, 'lxml')
        data = soup.find('div', {'class': 'wrapper-flat--H4DVL_qLjKLCo1sytcNI'})
        data1 = soup.find('div', {'class': 'vacancy-company-redesigned'})
        data2 = soup.find('div', {'class': 'g-user-content'})
        if data:
            position = data.find('h1', {'class': 'bloko-header-section-1'}).text
            salary = data.find('span', {'class': 'magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-label-1-regular___pi3R-_3-0-9'}).text
            description = data.find_all('p', {'class': 'vacancy-description-list-item'})
            experience = description[0].text
            schedule = description[1].text
            company = data1.find('span', {'class': 'bloko-header-section-2 bloko-header-section-2_lite'}).text
            address_element = data1.find('div', {'class': 'magritte-text___pbpft_3-0-9 magritte-text_style-primary___AQ7MW_3-0-9 magritte-text_typography-paragraph-2-regular___VO638_3-0-9'})
            address = address_element.find('p').text if address_element else None
            if address is None:
                address1_element = data1.find('span', {'class': 'magritte-text___tkzIl_4-1-4'})
                address = address1_element.find('span').text if address1_element else None
            print(position, salary, experience, schedule, company, address)
array()



