import scrapy
from ..items import ZhihuimagesItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/question/365419002/answer/997629941']

    def parse(self, response):
        image_list = response.css('div.QuestionAnswer-content img.origin_image::attr(src)').extract()
        for image_data in image_list:
            zhihu_item = ZhihuimagesItem()
            zhihu_item['image_src'] = image_data
            yield zhihu_item
