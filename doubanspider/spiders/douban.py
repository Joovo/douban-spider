# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import spiders, Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join

from urllib.parse import urlparse, urljoin
from doubanspider.items import DoubanspiderItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    home_page = 'https://movie.douban.com'
    start_urls = ['https://movie.douban.com/subject/27060077/reviews']

    def parse(self, response):
        # max_page for 绿皮书的影评 (4317)
        for next_page in range(0, 4000, 20):
            yield Request('{}?start={}'.format(self.start_urls[0], next_page))

        comment_url_list = response.xpath('//div[@class="main-bd"]/h2/a/@href').extract()
        for comment_url in comment_url_list:
            yield Request(comment_url, callback=self.parse_item)

    def parse_item(self, response):
        # item = DoubanspiderItem()
        # item['movie_name'] = '绿皮书'
        # item['movie_id'] = '27060077'
        # item['comment_head'] = response.xpath('//span[@property="v:summary"]/text()').extract_first()
        # item['comment_data'] = ''.join(response.xpath('//div[@id="review-content"]//text()').extract()).strip()
        # item['comment_url'] = response.url
        # item['people_name'] = response.xpath('//div[@id="review-content"]/@data-author').extract()

        item = ItemLoader(item=DoubanspiderItem(), response=response)
        # item.add_value('movie_name', '绿皮书')
        item.add_xpath('movie_name', '//header/a[2]/text()')
        item.add_value('movie_id', re.search('[0-9]+', response.url).group())
        item.add_xpath('comment_rate', '//span[contains(@class,"main-title-rating")]/@title')
        item.add_xpath('comment_head', '//span[@property="v:summary"]/text()')
        item.add_xpath('comment_data', '//div[@id="review-content"]//text()', Join())
        item.add_value('comment_url', response.url)
        item.add_xpath('people_name', '//div[@id="review-content"]/@data-author')

        return item.load_item()
