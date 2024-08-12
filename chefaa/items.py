# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChefaaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    prescription = scrapy.Field()
    stock = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
