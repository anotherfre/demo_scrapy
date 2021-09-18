# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
from .settings import IMAGES_STORE as IMST
from scrapy.exceptions import DropItem


class MuoumhPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def get_media_requests(self, item, info):
        image_url = item['img_url']
        yield scrapy.Request(url=image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        else:
            if not os.path.exists(IMST + '/' + item['chapter_title']):
                os.mkdir(IMST + '/' + item['chapter_title'])
            os.rename(IMST + '/' + results[0][1]['path'],
                      IMST + '/''/' + item['chapter_title'] + '/' + item['title'] + '.jpg')
