import scrapy
from JD.items import JdItem


class Jdssspider(scrapy.Spider):
    name = 'jdsn'
    allowed_domains = ['www.jd.comd.com']
    page = 3
    s = 56
    key = 'swith'
    nopass = False
    number = 2
    item = JdItem()
    start_urls = [f'https://search.jd.com/Search?keyword={key}&wq={key}&page={page}&s={s}']

    def parse(self, response):
        list_id = []
        pieces = 0

        print(response)
        print('——————————————————————开始爬取——————————————————————')
        print('——————————————————————开始输出——————————————————————')

        all = response.xpath('//div[@id="J_goodsList"]/ul/li')
        for i in all:
            id = i.xpath('./@data-sku').extract_first()
            url = 'https:' + i.xpath('.//div[@class="p-name p-name-type-2"]/a/@href').extract_first()
            title = i.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()').extract_first()
            shop = i.xpath('.//div[@class="p-shop"]/span/a/text()').extract_first()
            price = i.xpath('.//div[@class="p-price"]/strong/i/text()').extract_first()
            print(title, price)
            list_id.append(id)
            self.item['url'] = url
            self.item['title'] = title
            self.item['shop'] = shop
            self.item['price'] = price
            yield self.item
            pieces += 1
            print(f'当前为第{pieces}')

        url = [f"https://search.jd.com/Search?keyword={self.key}&wq={self.key}&page={self.page}&s={self.s}",
               f'https://search.jd.com/s_new.php?keyword={self.key}&page={self.page - 1}&show_items={",".join(list_id)}']
        headers = {"Referer": url}
        if self.nopass:
            self.nopass = False
            url = url[0]
            headers = None

        else:
            self.page += 2
            self.s += 60
            self.nopass = True
            url = url[1]
        print(f'当前为第{self.number}页')
        self.number += 1
        if self.number < 20 and pieces == 30:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=headers,
                dont_filter=True)
        else:
            return
