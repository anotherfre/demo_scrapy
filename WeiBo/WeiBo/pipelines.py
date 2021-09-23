# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem
import requests
import random
import string


class WeiboPipeline:
    def process_item(self, item, spider):
        response = requests.get(item['image_src'])
        image = response.content
        name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        path = 'D:\demo_code\demo_scrapy\WeiBo\WeiBo\IMAGES\{}.jpg'.format(name)
        with open(path, 'wb') as f:
            f.write(image)
        return item

    # def get_media_requests(self, item, info):
    #     yield scrapy.Request(url=item['image_src'])
    #
    # def item_completed(self, results, item, info):
    #     image_path = [x['path'] for ok, x in results if ok]
    #     if not image_path:
    #         raise DropItem('Image Download Failed')
    #     return item
