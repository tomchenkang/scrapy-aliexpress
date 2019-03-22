# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AliItem(scrapy.Item):
    file_urls = scrapy.Field()
    image_urls = scrapy.Field()
    specifics = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    pass

class IpItem(scrapy.Item):
	ttype = scrapy.Field()
	ip = scrapy.Field()
	port = scrapy.Field()