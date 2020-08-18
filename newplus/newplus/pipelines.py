# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import Redis


class RedisPipeline:
    conn = None

    def open_spider(self, spider):

        self.conn = Redis(host='127.0.0.1', port=6379)

    def process_item(self, item, spider):
        self.conn.lpush('news', item)
