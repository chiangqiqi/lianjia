# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import numpy as np

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from datetime import datetime

class lianjiaPipeline(object):
    def __init__(self):
        self.file = open('lianjia.csv', 'wb')
        self.file.write(
            'name_of_community' + ',' + 'layout_of_house' + ',' +
            'price_of_house' + ',' + 'area_of_house' + ',' +
            'floor_of_house' + ',' + 'time_of_construction' + '\n'
        )

    def get_value(self, value):
        value[0].strip()

    def process_item(self, item, spider):
    #该函数的作用有: 
        #1.将数据写入CSV文件 2.去除每个值的左右空格 
        #3.将每个值编码为utf8 4.以逗号当做分隔符
        if len(item['time_of_construction']) == 0:
            item['time_of_construction'].append('')
            item['time_of_construction'].append('')
        elif len(item['time_of_construction']) == 1:
            item['time_of_construction'].append('')
        else:
            pass

        # self.file.write(
            # item.values()
            # map(lambda x: self.get_value(x).encode('utf-8'), item.values()).join(",")
            #每个字段实际是一个列表, 如果只有一个值需要切片[0]取数
	    # item['name_of_community'][0].strip().encode('utf-8') + ',' +
        #     item['layout_of_house'][0].strip().encode('utf-8') + ',' +
        #     item['price_of_house'][0].strip().encode('utf-8') + ',' +
        #     item['area_of_house'][0].strip().encode('utf-8') + ',' + 
        #     #但是也有像下面的, 列表中有两个值, 正好拆开来存储为两个字段
        #     item['time_of_construction'][0].strip().encode('utf-8') + ',' + 
        #     item['time_of_construction'][1].strip().encode('utf-8') + '\n' 
        # )


        return item

    def spider_closed(self, spider):
        self.file.close()

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.datestr = datetime.now().strftime("%Y-%m-%d")

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            data = dict(item)
            self.collection.insert(data)
            log.msg("record added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
