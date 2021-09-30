# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
from pprint import pprint
import json

url = 'https://api.vk.com/method/users.get'
params = {
    'fields': 'photo_id,verified,sex,bdate,city,country,home_town',
    'v': 5.81,
    'access_token': ''
}

response = requests.get(url, params=params)
j_data = response.json()

with open('data_2.json', 'w', encoding='utf-8') as file:
    json.dump(j_data, file)
