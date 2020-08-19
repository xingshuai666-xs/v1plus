import scrapy
from newplus.items import NewplusItem
from time import sleep
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.6181"
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
            meta={'inp': inp, 'page': 1}
        )

    def parse(self, response):

        inp = response.meta['inp']
        page = response.meta['page']

        response = response.json()
        print(response)
        results = response['content']['results']
        if results:
            for i in results:
                item = NewplusItem()
                item['title'] = i['title']
                item['title_url'] = i['url']
                item['summary'] = i['des']
                url = i.get('imgUrl')
                if url:
                    item['img'] = "http://tpic.home.news.cn" + url
                item['time'] = i['pubtime']
                if item['title'] and item['title_url']:
                    yield item

            sleep(random.randint(1, 4))
            page += 1
            yield scrapy.Request(
                url=f'http://so.news.cn/getNews?keyword={inp}&curPage={page}&sortField=0&searchFields=1&lang=cn',
                headers=headers,
                callback=self.parse,
                meta={'page': page, 'inp': inp}
            )
