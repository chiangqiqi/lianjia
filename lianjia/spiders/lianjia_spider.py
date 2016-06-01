import scrapy
from lianjia.items import lianjiaItem
from datetime import datetime

class lianjiaSpider(scrapy.Spider):
    def __init__(self, args):
        "docstring"

        name = 'lianjia'
        allowed_domains = ["lianjia.com"]
        city_and_page = {
            'dongcheng': 99, 'cicheng': 100, 'chaoyang': 100, 'haidian': 100,
            'fengtai': 100, 'shijingshan': 96, 'tongzhou': 93, 'changping': 100,
            'daxing': 100, 'yizhuangkaifaqu': 52, 'shunyi': 100, 'fangshan': 100, 
            'mentougou': 49, 'pinggu': 0, 'huairou': 1, 'miyun': 1, 'yanqing': 1,
            'yanjiao': 100}

        house_type = "ershoufang"
        county = ["haidian", "chaoyang"]
        city = "bj"

        base_url = "http://{ct}.lianjia.com/{t}/{c}/pg%{n}"

        start_urls = []
        for i in xrange(1, 100):
            start_urls.append(base_url.format(ct=city, c=county, t=house_type, n=i+1))

        keyfunMap = {"name_of_community": "div[1]/div[1]/a/span/text()" ,
                     'layout_of_house': "div[1]/div[1]/span[1]/span/text()",
                     'price_of_house':  "div[2]/div[1]/span/text()",
                     'area_of_house': "div[1]/div[1]/span[2]/text()",
                     'time_of_construction': "div[1]/div[2]/div/text()"}

    def parse(self, response):
        for sel in response.xpath("//div[@class='info-panel']"):
            lianjia = lianjiaItem()
            for k,v in self.keyfunMap.items():
                lianjia[k] = sel.xpath(v).extract()[0].strip()

            lianjia["date"] = datetime.now().strftime('%Y-%m-%d')
            lianjia["city"] = self.city
            lianjia["county"] = self.county
            yield lianjia
