import scrapy
from newplus.items import NewplusItem
import json
import re
from time import sleep
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.6181",
    "Cookie": "userid=1592813646339_g7566s4236; UM_distinctid=173704778ca54e-0cebd9e9f03113-5f79591b-144000-173704778cb807"
}


class FenghuangSpider(scrapy.Spider):
    name = 'fenghuang'
    ym_sum = 0
    rank = 0

    def start_requests(self):
        inp = input('>>>')
        yield scrapy.Request(
            url=f'https://shankapi.ifeng.com/autumn/getSoFengData/all/{inp}/1/getSoFengDataCallback?callback=getSoFengDataCallback&_=15974592577480',
            headers=headers,
            callback=self.parse,
            meta={'inp': inp, 'ym': 0}
        )

    def parse(self, response):

        inp = response.meta['inp']
        ym = response.meta['ym']

        response = json.loads(re.search(r'{.*}', response.text).group())
        print(response)
        if self.ym_sum == 0:
            self.ym_sum = response['data']['totalPage']

        for i in response['data']['items']:

            item = NewplusItem()
            item['title'] = i['title'].replace('<em>', '').replace('</em>', '')
            url = i.get('url')
            if url:
                item["title_url"] = "https:" + url
            else:
                item['title_url'] = ''
            img = i.get('thumbnails')
            if img != None:
                for ii in img['image']:
                    item['img'] = ii['url']
            else:
                item['img'] = ''
            if item['title'] and item['title_url']:
                self.rank += 1
                yield item

        ym += 1
        sleep(random.randint(1, 4))
        if ym < self.ym_sum:
            yield scrapy.Request(
                url=f'https://shankapi.ifeng.com/autumn/getSoFengData/all/{inp}/{ym}/getSoFengDataCallback?callback=getSoFengDataCallback&_=15974592577480',
                headers=headers,
                callback=self.parse,
                meta={'ym': ym, 'inp': inp}
            )
