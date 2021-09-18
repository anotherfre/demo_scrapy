import scrapy
import re
import random
import string
from ..items import MuoumhItem


class MuouSpider(scrapy.Spider):
    name = 'MuOu'
    allowed_domains = ['www.gllmh.com']
    start_urls = ['http://www.gllmh.com/slygsh/']
    target_urls = []

    def parse(self, response):

        # 获取每一章节链接
        src_list = response.css('div.viewimg a.zzsz::attr(href)').extract()
        if src_list:
            for src in src_list:
                chapter_url = response.urljoin(src)
                yield scrapy.Request(url=chapter_url, callback=self.parse)

        # 获取每一页链接
        chapter_page_url = response.css('div.page li a::attr(href)').extract()
        if chapter_page_url:
            for page_url in chapter_page_url:
                page_href = response.urljoin(page_url)
                if page_href not in self.target_urls:
                    # print('************page_href**************', page_href)
                    self.target_urls.append(page_href)
                    yield scrapy.Request(url=page_href, callback=self.parse)

        img_src_list = response.css('div.article-content.fontSizeSmall.BSHARE_POP p img').extract()
        chapter_title = response.css('div.listltitle h3::text').extract_first()
        chapter_title = str(chapter_title).split('》')[0] + '》'
        if img_src_list:
            for img_cont in img_src_list:
                title = re.findall(r'title="(.*?)"', img_cont)
                img = re.findall(r'src="(.*?)"', img_cont)

                xs_item = MuoumhItem()
                xs_item['chapter_title'] = chapter_title
                if title:
                    xs_item['title'] = title[0]
                else:
                    xs_item['title'] = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                if img:
                    xs_item['img_url'] = img[0]
                else:
                    xs_item['img_url'] = ""

                yield xs_item

        next_page = response.css('div.pagination li a').extract()
        if next_page:
            next_page_url = re.findall(r'href="(.*?)"', next_page[-1])
            page_url = response.urljoin(next_page_url[0])
            yield scrapy.Request(url=page_url, callback=self.parse)
