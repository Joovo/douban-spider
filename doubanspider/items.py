# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class DoubanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Field()
    movie_id = Field()
    movie_name = Field()

    comment_url = Field()
    comment_rate = Field()
    comment_head = Field()
    comment_data = Field()


    people_name = Field()
