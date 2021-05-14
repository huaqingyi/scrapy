from scrapy.spiders import Spider
from scrapy import Request
from numpy import arange


class AcFunSpider(Spider):
    name = 'AcFun'
    start_urls = [
        'https://www.acfun.cn/v/list120/index.htm?sortField=rankScore&duration=all&date=default&page=1']
    page = []

    def parse(self, response):
        list = response.xpath('//div[@id="listwrapper"]')[0].xpath(
            './div[@class="list-wrapper"]').xpath('./div[@class="list-content-item"]')

        page = []
        for row in list:
            data = {}
            top = row.xpath('./a[@class="list-content-top"]')[0]
            data['count'] = top.xpath(
                './div[@class="list-content-data"]/span[@class="viewCount"]/text()')[0].extract().strip()
            data['commentCount'] = top.xpath(
                './div[@class="list-content-data"]/span[@class="commentCount"]/text()')[0].extract().strip()
            data['src'] = top.css('img::attr(src)')[0].extract()
            data['title'] = row.xpath(
                './h1[@class="list-content-title"]/a/text()')[0].extract().strip()
            data['up'] = row.xpath(
                './a[@class="list-content-uplink"]/text()')[0].extract().strip()
            page.append(data)

        self.page.append(page)
        
        pages = arange(2, 5, 1)
        for p in pages:
            url = 'https://www.acfun.cn/v/list120/index.htm?sortField=rankScore&duration=all&date=default&page=%s'%(p)
            yield Request(url, self.parse)

        print(self.page)
