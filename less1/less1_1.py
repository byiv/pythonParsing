# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.
import requests
from pprint import pprint
import json

user = input('Введите имя пользователя github: ')
url = f'https://api.github.com/users/{user}/repos'
headers = {'Accept': 'application/vnd.github.v3+json'}


response = requests.get(url, headers = headers)
j_data = response.json()

for i in j_data:
    print(f"Repo name: {i['name']}, url: {i['url']}")

with open('data.json', 'w') as file:
    json.dump(j_data, file)
