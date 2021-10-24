# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def clear_price(value):
    try:
        value = int(value.replace(' ', ''))
    except:
        return value
    return value


def clear_specifications_dd(value):
    try:
        value = value.replace('\n', '').strip()
    except:
        return value
    return value

class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    print()
    link = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    photo = scrapy.Field()
    specifications_dd = scrapy.Field(input_processor=MapCompose(clear_specifications_dd))
    specifications_dt = scrapy.Field()
    specifications = scrapy.Field()
    _id = scrapy.Field()
