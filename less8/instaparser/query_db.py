from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client.instagramm

find_users = db.list_collection_names()
types_friend = ['following', 'followers']
for tp in types_friend:
    print(f'{types_friend.index(tp)} - {tp}')
type_friend_ind = int(input(f'Укажите тип отбора: '))
for user in find_users:
    print(f'{find_users.index(user)} - {user}')
find_user_ind = int(input(f'Выберите номер пользователя: '))
type_friend = types_friend[type_friend_ind]
find_user = find_users[find_user_ind]
docs = db[find_user].find({'type_friend': type_friend})
for doc in docs:
    print(f"{doc['user_name']}")
