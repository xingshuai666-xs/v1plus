import scrapy
from JD.items import JdItem
from time import sleep


class FenghuangSpider(scrapy.Spider):
    name = 'zwqb'
    start_urls = [f'http://www.530p.com/s/斗破/1/']
    novel_list = []

    def parse(self, response):
        page_id = response.xpath('//div[@id="pagebav"]/a/@href').extract()
        for url in page_id:
            page_url = f'http://www.530p.com{url}'
            # print(page_url)
            print(url)
            yield scrapy.Request(
                url=page_url,
                callback=self.novel,
                dont_filter=True,
            )

    def novel(self, response):
        print("执行页码级别")
        all = response.xpath('//div[@class="conter"]/ul')
        for i in all:
            try:
                title = i.xpath('./li[@class="conter1"]//text()').extract_first()
                url = i.xpath('./li[@class="conter1"]/a/@href').extract_first()
                author = i.xpath('./li[@class="conter4"]//text()').extract_first()
                time = i.xpath('./li[@class="conter3"]//text()').extract_first()
                self.novel_list.append([title, f'http://www.530p.com{url}', author, time])
                print(title)
            except Exception:
                continue
        print(self.novel_list[1][1])
        yield scrapy.Request(
            url=self.novel_list[1][1],
            callback=self.chapter_url,
            dont_filter=True,
        )

    def chapter_url(self, response):
        # 章节级别
        self.chapters_list = []
        print("执行章节级别yield")
        chapter_first = response.xpath('//div[@class="clc"]/a')
        author = response.xpath('//td[@class="tc"][1]//text()').extract_first()
        category = response.xpath('//td[@class="tc"][2]//text()').extract_first()
        time = response.xpath('//td[@class="tc"][3]//text()').extract_first()
        for i in chapter_first:
            url_i = i.xpath('./@href').extract_first()
            url = f'http://www.530p.com{url_i}'
            print(url_i)
            self.chapters_list.append(url)
        print(self.chapters_list)
        a = 1
        for url in self.chapters_list:
            try:
                print(url, '章节url')
                print(a)
                a+=1
                yield scrapy.Request(url=url,
                                     callback=self.text,
                                     meta={'url': url, 'author': author, 'category': category, 'time': time},
                                     dont_filter=True)
            except Exception:
                continue

    def text(self, response):

        # 正文级别
        item = JdItem()
        print("执行正文级别yield")
        a =1
        try:
            nevelone_title = response.xpath('//td[@class="bav_border_top"][1]/a[3]//text()').extract_first()
            text_title = response.xpath('//div[@id="cps_title"]//text()').extract_first()
            text_text = response.xpath('//div[@id="cp_content"]//text()').extract()
            item['title'] = nevelone_title
            item['url'] = response.meta['url']
            item['author'] = response.meta['author']
            item['time'] = response.meta['time']
            item['category'] = response.meta['category']
            item['text_title'] = text_title
            item['text_text_all'] = item['title'] + ''.join(text_text).replace('\u3000\u3000', '').strip('\r\n')
            print(item['title'])
            print(a)
            a+=1
            yield item
        except Exception:
            pass
