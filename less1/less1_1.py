import requests
from pprint import pprint

user = 'byiv'
url = f'https://api.github.com/users/{user}/repos'

response = requests.get(url)
j_data = response.json()
pprint(j_data)











