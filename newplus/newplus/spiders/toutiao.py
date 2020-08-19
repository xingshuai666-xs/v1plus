import scrapy
from newplus.items import NewplusItem
from time import sleep
import random

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.6181"
}


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    # allowed_domains = ['www.xxx.com']
    offset_sum = 0
    rank = 0

    def start_requests(self):
        inp = input('>>>')
        yield scrapy.Request(
            url=f'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword={inp}autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1597799189984&_signature=zH0lwAAgEBCfLpFW--m0q8x8ZNAAJNKmXstFWYfGMyqNu9Go9JHflsYpoxLimW8QDZkA41Hh8NpXx53JW4J6qYSnLB.jexWrWs3gGINWukxlQR.4CWV1YDWo5arz0DrLxwe',
            headers=headers,
            callback=self.parse,
            meta={'inp': inp, 'offset': 0}
        )

    def parse(self, response):

        inp = response.meta['inp']
        offset = response.meta['offset']

        response = response.json()
        print(response)
        self.offset_sum = response['offset']
        data = response.get('data')
        print(data)
        if data:

            for i in data:
                quan = False
                item = NewplusItem()

                if i.get('abstract') and i.get('datetime') and i.get('article_url'):
                    item['title'] = i['abstract']
                    item['time'] = i['datetime']
                    item['title_url'] = i['article_url']
                    quan = True

                if i.get('img_url'):
                    item['img'] = i['image_url']
                if quan:
                    # quan = False
                    self.rank += 1
                    yield item

            sleep(random.randint(1, 4))
            offset += 20
            yield scrapy.Request(
                url=f'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={offset}&format=json&keyword={inp}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1597799189984&_signature=zH0lwAAgEBCfLpFW--m0q8x8ZNAAJNKmXstFWYfGMyqNu9Go9JHflsYpoxLimW8QDZkA41Hh8NpXx53JW4J6qYSnLB.jexWrWs3gGINWukxlQR.4CWV1YDWo5arz0DrLxwe',
                headers=headers,
                callback=self.parse,
                meta={'offset': offset, 'inp': inp}
            )
