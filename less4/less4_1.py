from pprint import pprint
from lxml import html
import requests

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news']
news_ya = db.news_ya

header = {'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
          '(KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}

response = requests.get("https://yandex.ru/news/")
dom = html.fromstring(response.text)

items = dom.xpath("//article")

# all_news = []

for item in items:
    news = {}
    name = item.xpath(".//h2/text()")[0]
    link = item.xpath(".//a[@class='mg-card__link']/@href")[0]
    text = item.xpath(".//div[@class='mg-card__annotation']/text()")[0]
    source = item.xpath(".//a[@class='mg-card__source-link']/text()")[0]
    source_link = item.xpath(".//a[@class='mg-card__source-link']/@href")[0]
    source_time = item.xpath(".//span[@class='mg-card-source__time']/text()")[0]

    news['name'] = name
    news['link'] = link
    news['text'] = text
    news['source'] = source
    news['source_link'] = source_link
    news['source_time'] = source_time
    news_ya.insert_one(news)
