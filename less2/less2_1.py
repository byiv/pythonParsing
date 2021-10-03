# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH(обязательно)
# и/или Super job(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

# https://hh.ru/vacancies/programmist
import json

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re

position = 'Программист Python'
url = 'https://hh.ru'
params = {
    'page': 0,
    # 'customDomain': 1,
    'text': position
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/93.0.4577.82 Safari/537.36'}

position_data = []

while True:

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    # print(response.url)
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
        vacancy_data['id'] = vacancy_id
        vacancy_data['site_url'] = url
        vacancy_data['salary_min'] = vacancy_salary_min
        vacancy_data['salary_max'] = vacancy_salary_max
        vacancy_data['salary_currency'] = vacancy_salary_currency

        position_data.append(vacancy_data)

    if not soup.find('a', text='дальше') or not response.ok:
        break

    params['page'] += 1

with open('vacancy_data.json', 'w') as file_json:
    json.dump(position_data, file_json)

