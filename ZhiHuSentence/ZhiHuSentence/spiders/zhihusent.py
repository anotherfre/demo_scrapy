import scrapy
from ..items import ZhihusentenceItem


class ZhihusentSpider(scrapy.Spider):
    name = 'zhihusent'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/question/318185970/answer/742914625']

    def parse(self, response):
        sentences_type_1 = response.xpath('//blockquote').extract()
        sentences_type_2 = response.xpath("//div[@class='RichContent-inner']//p/text()").extract()
        sentences_sum = sentences_type_1 + sentences_type_2
        for sentence in sentences_sum:
            sent_item = ZhihusentenceItem()
            sent_item['sentence'] = sentence
            yield sent_item
