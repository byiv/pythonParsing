import requests
from pprint import pprint

user = 'byiv'
url = f'https://api.github.com/users/{user}/repos'
headers = {'Accept': 'application/vnd.github.v3+json'}


response = requests.get(url, headers = headers)
j_data = response.json()

pprint(j_data)
