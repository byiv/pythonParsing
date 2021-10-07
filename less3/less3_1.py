# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию.
# Добавить в решение со сбором вакансий(продуктов) функцию,
# которая будет добавлять только новые вакансии/продукты в вашу базу.

from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import re
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacancy']
vacancy_hh = db.vacancy_hh
vacancy_hh.delete_many({})

position = 'Программист Python'
url = 'https://hh.ru'
params = {
    'page': 0,
    # 'customDomain': 1,
    'text': position
}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

while True:
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    position_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    for vacancy in position_list:
        vacancy_data = {}
        vacancy_info = vacancy.find('a', attrs={'class': 'bloko-link'})

        vacancy_name = vacancy_info.text
        vacancy_link = vacancy_info['href']
        vacancy_id = re.search(r'y/(.+?)\?', vacancy_link).group(1)

        vacancy_salary = None
        vacancy_salary_min = None
        vacancy_salary_max = None
        vacancy_salary_currency = None

        try:
            vacancy_salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            vacancy_salary = vacancy_salary.replace('\u202f', '')
            vacancy_salary = re.split(r'\s', vacancy_salary)

            vacancy_salary_currency = vacancy_salary[-1]
            if vacancy_salary[0] == 'от':
                vacancy_salary_min = int(vacancy_salary[1])
            elif vacancy_salary[0] == 'до':
                vacancy_salary_min = int(vacancy_salary[1])
            else:
                vacancy_salary_min = int(vacancy_salary[0])
                vacancy_salary_max = int(vacancy_salary[2])
        except:
            pass

        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['_id'] = vacancy_id
        vacancy_data['site_url'] = url
        vacancy_data['salary_min'] = vacancy_salary_min
        vacancy_data['salary_max'] = vacancy_salary_max
        vacancy_data['salary_currency'] = vacancy_salary_currency

        # Поиск дублей по _id, если нет то вставка новой записи
        vacancy_hh.update_one({'_id': vacancy_data['_id']}, {'$set': vacancy_data}, True)

    if not soup.find('a', text='дальше') or not response.ok:
        break

    params['page'] += 1

result = vacancy_hh.count_documents({})
pprint(result)
