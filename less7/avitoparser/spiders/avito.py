import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://www.avito.ru/rossiya/?q={query}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-marker="item-title"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)
        print()
        pass

    def parse_ads(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1/span/text()").get()
        price = response.xpath("//span[@itemprop='price']/text()").get()


        print()


