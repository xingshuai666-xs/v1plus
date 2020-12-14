# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()  # 价格
    shop = scrapy.Field()  # 店铺
    author = scrapy.Field()  # 作者
    category = scrapy.Field()  # 类别
    time = scrapy.Field()
    text_title = scrapy.Field()
    text_text_all = scrapy.Field()
