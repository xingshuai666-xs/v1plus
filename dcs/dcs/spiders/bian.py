from scrapy_redis.spiders import RedisSpider
import scrapy
from dcs import items
import random
from time import sleep

headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.6181"

}


class XinhuaSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'xinhuas'
    redis_key = 'xinhua:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(XinhuaSpider, self).__init__(*args, **kwargs)
        self.url = 'http://so.news.cn/getNews?keyword={}&curPage={}&sortField=0&searchFields=1&lang=cn'

    def make_request_from_data(self, datas):
        inp = input('>>>')
        return scrapy.Request(
            self.url.format(inp,1),
            meta={'inp': inp, 'page': 1, 'rank': 0},
            headers=headers,
            callback=self.parse
        )

    def parse(self, response):
        inp = response.meta['inp']
        page = response.meta['page']
        rank = response.meta['rank']

        response = response.json()
        print(response)
        results = response['content']['results']
        if results:
            for i in results:
                item = items.ExampleItem()
                item['title'] = i['title']
                item['title_url'] = i['url']
                item['summary'] = i['des']
                url = i.get('imgUrl')
                if url:
                    item['img'] = "http://tpic.home.news.cn" + url
                item['time'] = i['pubtime']
                if item['title'] and item['title_url']:
                    rank+=1
                    yield item
            print(f'当前数据为{rank}条')
            # sleep(random.randint(1, 4))
            page += 1
            yield scrapy.Request(
                self.url.format(inp,page),
                meta={'inp': inp, 'page': page, 'rank': rank},
                headers=headers,
                callback=self.parse
            )

