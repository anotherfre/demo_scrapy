import scrapy
from ..items import OnepunchItem
import urllib
import random
import os


class OnePunchSpider(scrapy.Spider):
    name = 'one_punch'
    allowed_domains = ['https://tieba.baidu.com/p/7422468467?see_lz=1']
    start_urls = ['https://tieba.baidu.com/p/7422468467?see_lz=1']

    def parse(self, response):
        src_list = response.css('.BDE_Image::attr(src)').extract()
        for src in src_list:
            item = OnepunchItem()
            item['src'] = [src]
            file_path = os.path.join(r"D:\cartoon", str(random.randint(1, 1000)) + '.jpg')
            urllib.request.urlretrieve(src, file_path)
            yield item

