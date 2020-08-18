import scrapy
from newplus.items import NewplusItem
from time import sleep
import random

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.6181"
}


class ToutiaoSpider(scrapy.Spider):
    name = 'xinhua'
    offset_sum = 0
    rank = 0

    def start_requests(self):
        inp = input('>>>')
        yield scrapy.Request(
            url=f'http://so.news.cn/getNews?keyword={inp}&curPage=1&sortField=0&searchFields=1&lang=cn',
            headers=headers,
            callback=self.parse,
            meta={'inp': inp}
        )

    def parse(self, response):

        inp = response.meta['inp']

        response = response.json()
        print(response)
        for i in response['content']['results']:
            item = NewplusItem()
            item['title'] = i['title']
            item['title_url'] = i['url']
            item['summary'] = i['des']
            url = i.get('imgUrl')
            if url:
                item['img'] = "http://tpic.home.news.cn" + url
            item['time'] = i['pubtime']

        # if offset < self.offset_sum:
        yield scrapy.Request(
            url=f'http://so.news.cn/getNews?keyword={inp}&curPage=1&sortField=0&searchFields=1&lang=cn',
            headers=headers,
            callback=self.parse,
            # meta={'offset': offset}
        )
