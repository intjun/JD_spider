# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import json
import requests
import os
from hashlib import md5
from JD_spider.items import JdSpiderItem

class JdSpider(scrapy.Spider):
    name = 'JD'
    allowed_domains = ['re.jd.com/search']
    start_urls = 'https://re.jd.com/search'

    def start_requests(self):
        url = '{url}?keyword={keyword}&page={page}'.format(url=self.start_urls,keyword='车',page='1')
        yield Request(url,callback=self.parse,meta={'keyword':'车'})


    def parse(self, response):
        keyword = response.meta['keyword']
        wares_pattern = re.compile('var pageData = (.*?),"retest"', re.S)
        result = re.search(wares_pattern, response.text)
        # print(result.group(1)+'}')
        # print(len(result.group(1)))
        pro_data = result.group(1) + '}'
        data = json.loads(pro_data)
        # print(data.keys())
        total = data['summary']['total']  # data.get('summary')
        page = data['summary']['page']
        page_count = data['summary']['pagecount']
        print(total, page, page_count)
        results = data['result']
        for result in results:
            title = result['ad_title_text']
            # https://img1.360buyimg.com/n6/jfs/t27397/57/2225126831/335914/c1b23b3f/5bfba4a0N52abfc52.png
            image = 'https://img1.360buyimg.com/n6/' + result['image_url']
            price = result['sku_price']
            comment_num = result['commentnum']
            good_count = result['good_count']
            good_rate_show = result['good_rate_show']
            url = result['click_url']
            # flags = result['flages']
            file_path = self.download_img(image)
            JD_item = JdSpiderItem()
            for field in JdSpiderItem.fields:
                try:
                    JD_item[field] = eval(field)
                except NameError:
                    self.logger.debug('Field is Not Defined ' + field)

            yield JD_item

    def download_img(self,url):
        print('正在下载', url)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = self.save_img(response.content)
                return file_path
        except:
            print('请求图片出错', url)
            return None

    def save_img(self,content):
        img_path = 'G:/Pycharm/JD_spider/img'
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        file_path = 'G:/Pycharm/JD_spider/img/{}.{}'.format(md5(content).hexdigest(), 'jpg')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(content)
                f.close()
        return file_path