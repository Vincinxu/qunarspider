import requests
from requests.exceptions import RequestException
from lxml import etree
from urllib.parse import quote
import pymongo


class QunarSpider():
    #初始化
    def __init__(self, keyword, max_page, mongo_uri):
        self.keyword = keyword
        self.page = max_page
        self.mongo_uri = mongo_uri
        self.mongo_db = 'qunarspider'
        self.mongo_collection = 'qunar'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }
    
    
    #获取页面
    def get_page(self, page):
        try:
            url = 'https://piao.qunar.com/ticket/list_'+ quote(self.keyword) +'.html?keyword='+ quote(self.keyword) +'&page='+ str(page)
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None
    
    
    #解析页面，提取数据
    def parse_page(self, html):
        text = etree.HTML(html)
        items = text.xpath('//div[contains(@class, "sight_item_detail")]')
        for item in items:
            yield {
                'image': item.xpath('div[@class="sight_item_show"]//img/@data-original'),
                'title': item.xpath('div[@class="sight_item_about"]/h3/a/text()'),
                'level': item.xpath('div[@class="sight_item_about"]/div//span[@class="level"]/text()'),
                'area': item.xpath('div[@class="sight_item_about"]/div//span[@class="area"]/a/text()'),
                'address': item.xpath('div[@class="sight_item_about"]//p/span/text()'),
                'desc': item.xpath('div[@class="sight_item_about"]//div[contains(@class, "intro")]/text()'),
                'price': item.xpath('div[@class="sight_item_pop"]//span[@class="sight_item_price"]/em/text()'),
                'soldnum': item.xpath('div[@class="sight_item_pop"]//span[@class="hot_num"]/text()'),
            }

    
    #保存到mongodb
    def save_to_mongodb(self, content):
        self.client = pymongo.MongoClient(self.mongo_uri)
        db = self.client[self.mongo_db]
        db[self.mongo_collection].insert(dict(content))
        print(content)
    
    #关闭mongodb
    def close(self):
        self.client.close()

    #运行
    def run(self):
        try:
            for i in range(1, self.page + 1):
                html = self.get_page(i)
                content =self.parse_page(html)
                for item in content:
                    self.save_to_mongodb(item)
            self.close()
        except:
            print('保存失败')


if __name__ == '__main__':
    QunarSpider('深圳', 39, 'localhost').run()

