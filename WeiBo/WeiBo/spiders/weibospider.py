import scrapy
from ..items import WeiboItem


class WeibospiderSpider(scrapy.Spider):
    name = 'weibospider'
    allowed_domains = ['weibo.com']
    start_urls = ['https://m.weibo.cn/u/7567091949?tabtype=album%3Ftabtype%3Dalbum&tabtype=album&jumpfrom=weibocom']

    def parse(self, response):

        data_list = response.xpath("//ul[@class='m-auto-list']")
        for data in data_list:
            images = data.xpath(".//li//img/@src").extract()
            for img in images:
                item = WeiboItem()
                item['image_src'] = img
                yield item
