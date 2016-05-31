# -*- coding: utf-8 -*-

# Scrapy settings for lianjia project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'lianjia'

SPIDER_MODULES = ['lianjia.spiders']
NEWSPIDER_MODULE = 'lianjia.spiders'

ITEM_PIPELINES = {
    'lianjia.pipelines.lianjiaPipeline' : 1,
    'lianjia.pipelines.MongoDBPipeline': 1
}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "lianjian"
MONGODB_COLLECTION = "ershoufang"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lianjia (+http://www.yourdomain.com)'
