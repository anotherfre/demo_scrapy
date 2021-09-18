import scrapy
from ..items import AnjukeItem
from ..settings import MAX_PAGE


class AjkSpider(scrapy.Spider):
    name = 'ajk'
    allowed_domains = ['xm.zu.anjuke.com/']
    start_urls = ['https://xm.zu.anjuke.com/']

    def start_requests(self):
        base_url = 'https://xm.zu.anjuke.com/fangyuan/p'
        for page in range(1, MAX_PAGE + 1):
            url = base_url + str(page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        list_content = response.xpath("//div[@class='list-content']/div[@class='zu-itemmod']")
        for content in list_content:
            title = content.xpath(".//a/b/text()").extract_first()
            size = content.xpath(".//p[@class='details-item tag']/b/text()").extract()
            size = size[0] + '室' + size[1] + '厅' + size[2] + '平米'
            contact = content.xpath(".//p[@class='details-item tag']/text()").extract()[5]
            price = content.xpath(".//div[@class='zu-side']//b/text()").extract_first()
            place = content.xpath(".//address/text()").extract()[1].replace('\n', '').strip()
            href = content.xpath(".//a/@href").extract_first()
            area = place[0:2]

            item = AnjukeItem()
            item['title'] = title
            item['size'] = size
            item['contact'] = contact
            item['price'] = price
            item['place'] = place
            item['area'] = area
            item['href'] = href
            yield item

        # next_page = response.xpath("//a[@class='aNxt']/@href").extract_first()
        #
        # url = response.urljoin(next_page)
        # yield scrapy.Request(url=url, callback=self.parse)
