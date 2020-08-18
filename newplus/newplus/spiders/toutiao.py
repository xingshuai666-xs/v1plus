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
            url=f'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword={inp}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1597732729923&_signature=8bCyUAAgEBCi4wbGgWG2OPGx80AAK6WCDVEgoxrWfT8UOk.foFSygFhig8d.Q6XiQb6scqZNK4iqpMxSaSMfUU7XY0S79xPeXKvjNzC1U8Q7IUwg0h38Nly3yz0Xb.QwG5U',
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
        if response['data'] != '':
            for i in response['data']:
                item = NewplusItem()
                item['title'] = i['title']
                item['time'] = i['datetime']
                item_id = i.get('item_id')
                if item_id:
                    item['title_url'] = "https://www.toutiao.com/group/" + item_id
                else:
                    item['title_url'] = ''
                item['img'] = i['image_url']
                if item['title'] and item['time'] and ['title_url']:
                    self.rank += 1
                    yield item

            sleep(random.randint(1, 4))
            offset += 20
            yield scrapy.Request(
                url=f'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={offset}&format=json&keyword={inp}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1597732729923&_signature=8bCyUAAgEBCi4wbGgWG2OPGx80AAK6WCDVEgoxrWfT8UOk.foFSygFhig8d.Q6XiQb6scqZNK4iqpMxSaSMfUU7XY0S79xPeXKvjNzC1U8Q7IUwg0h38Nly3yz0Xb.QwG5U',
                headers=headers,
                callback=self.parse,
                meta={'offset': offset, 'inp': inp}
            )
