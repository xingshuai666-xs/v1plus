# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewplusItem(scrapy.Item):
    title = scrapy.Field()
    title_url = scrapy.Field()
    time = scrapy.Field()
    img = scrapy.Field()
    summary = scrapy.Field()
    author = scrapy.Field()
