import scrapy
from newplus.items import NewplusItem
import json
import re
from time import sleep
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.6181",
}


class FenghuangSpider(scrapy.Spider):
    name = '32zhongwen'
    ym_sum = 0

    # rank = 0

    def start_requests(self):
        inp = input('>>>')
        yield scrapy.Request(
            url=f'http://www.530p.com/s/{inp}',
            headers=headers,
            callback=self.parse,
            meta={'inp': inp, 'ym': 1, 'rank': 0}
        )

    def parse(self, response):
        inp = response.meta['inp']
        ym = response.meta['ym']
        rank = response.meta['rank']

        # response.encoding = 'gbk'
        # response = response.text
        div = response.xpath('//div[@class="conter"]/ul')
        for i in div[1:]:
            item = NewplusItem()
            title = i.xpath('./li[@class="conter1"]/a/text()').extract_first()
            title_url = i.xpath('./li[@class="conter1"]/a/@href').extract_first()
            author = i.xpath('./li[@class="conter4"]/text()').extract_first()

            if title and title_url and author:
                item["title"] = title
                print(title)
                item["title_url"] = 'http://www.530p.com' + title_url
                item["author"] = author
                rank += 1
                yield item

        ym += 1
        print(ym)
        sleep(random.randint(1, 4))
        if rank == 30:

            yield scrapy.Request(
                url=f'http://www.530p.com/s/{inp}/{ym}/',
                headers=headers,
                callback=self.parse,
                meta={'ym': ym, 'inp': inp, 'rank': 0}
            )
# http://www.530p.com/s/%E6%AD%A6%E9%81%93/3/