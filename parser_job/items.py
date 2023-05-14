# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectParserHhItem(scrapy.Item):
    name = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()


class ProjectParserSuperItem(scrapy.Item):
    name = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
