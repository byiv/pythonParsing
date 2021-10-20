import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@rel="next" and contains(.,"Дальше")]').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//div[@class="_2rfUm _2hCDz _21a7u"]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath('//h1/text()').get()
        salary = response.xpath('//span[@class="_2Wp8I _2rfUm _2hCDz"]/text()').getall()
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item