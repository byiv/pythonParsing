# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с
# заработной платой больше введённой суммы (необходимо анализировать оба поля
# зарплаты - минимальнную и максимульную).

from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacancy']
vacancy_hh = db.vacancy_hh

salary = 400000

for doc in vacancy_hh.find({'$or': [{'salary_min': {'$gt': salary}}, {'salary_max': {'$gt': salary}}]}):
    pprint(doc)
