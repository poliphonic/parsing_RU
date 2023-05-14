# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserBooksItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    rating = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
