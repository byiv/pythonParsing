# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.vacansy1610

    def process_item(self, item, spider):
        item['salary_min'], item['salary_max'], item['currency'] = self.process_salary(item['salary'])
        del item['salary']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        salary_min = None
        salary_max = None
        currency = None
        # Провера hhru
        if len(salary) == 7:
            salary_min = salary[1].replace('\xa0', '')
            salary_max = salary[3].replace('\xa0', '')
            currency = salary[5]
        if len(salary) == 5:
            if salary[0] == 'от':
                salary_min = salary[1].replace('\xa0', '')
            if salary[0] == 'до':
                salary_max = salary[3].replace('\xa0', '')
            currency = salary[3]
        #  Проверка для sjru
        if len(salary) == 3:
            if salary[0] == 'до':
                salary_max = salary[2].replace('\xa0', '', 1)
                salary_max, currency = salary_max.split('\xa0')
            elif salary[0] == "от":
                salary_min = salary[2].replace('\xa0', '', 1)
                salary_min, currency = salary_min.split('\xa0')
            else:
                salary_min = salary_max = salary[0].replace('\xa0', '', 1)
                currency = salary[2]
            print()
        if len(salary) == 4:
            salary_min = salary[0].replace('\xa0', '')
            salary_max = salary[1].replace('\xa0', '')
            currency = salary[3]


        return salary_min, salary_max, currency

