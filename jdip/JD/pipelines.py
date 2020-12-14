# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import Redis
from JD.spiders import jdsn

class JdPipeline:
    def process_item(self, item, spider):
        return item


class RedisPlieLine:
    conn = None

    def open_spider(self, spider):
        self.conn = Redis(host='127.0.0.1', port=6379)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.conn.lpush(jdsn.Jdssspider().key, str(item))


class ZhongwenPlieLine:
    conn = None

    def open_spider(self, spider):
        self.conn = Redis(host='127.0.0.1', port=6379)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # self.conn.lpush(zhongwentwo.FenghuangSpider().Key, str(item))
        self.conn.lpush(f'<<{item["title"]}>>{item["author"]}', str(item))
        # self.conn.lpush('小说', str(item))