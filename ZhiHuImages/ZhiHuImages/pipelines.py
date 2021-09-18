# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem
import pymysql
import datetime
from ..local_settings import *


class ZhihuimagesPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     print('######################### this item pipeline##################################')
    #     return item

    def get_media_requests(self, item, info):
        # print('######################get_media_requests########################################')
        yield scrapy.Request(url=item['image_src'])

    def item_completed(self, results, item, info):
        # print('#######################item_completed   #####################################')
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Image Download Failed')
        return item


class mysqlPipeline:
    def __init__(self):
        self.host = HOST
        self.database = DATABASE
        self.user = USER
        self.password = PASSWORD
        self.port = PORT

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                  charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        create_time = datetime.datetime.now()
        sql = ''' insert into zhihu_image(image, del_flag, create_time) values(%s, %s, %s)'''
        try:
            self.cursor.execute(sql, (data['image_src'], 0, create_time))
            self.db.commit()
        except Exception as ex:
            self.db.rollback()
            print(ex)

    def close_spider(self, spider):
        self.db.close()
