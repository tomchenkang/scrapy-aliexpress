# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
import re
import json
from ali.items import AliItem, IpItem

class ExpressSpider(scrapy.Spider):
	name = 'express'
	allowed_domains = ['www.aliexpress.com']
	start_urls = ['https://www.aliexpress.com/',]

	def parse(self, response):
		#获取不同类别产品的网址
		categories = response.css('dt.cate-name a::text').getall()
		cate_urls = response.css('dt.cate-name a::attr(href)').getall()
		for i in range(len(cate_urls)):
			category = categories[i].strip()
			url = urljoin(self.start_urls[0], cate_urls[i])
			yield scrapy.Request(url, callback=self.parse_first,
				meta={'category': category,})

	def parse_first(self, response):
		#获取不同类别所有产品网址
		goods_urls = response.css('a.product::attr(href)').getall()[:2]
		for url in goods_urls:
			url = urljoin(self.start_urls[0], url)
			yield scrapy.Request(url, callback=self.parse_second, meta=response.meta)
		next_page = response.css('a.page-next::attr(href)').get()
		next_page = urljoin(self.start_urls, next_page)
		yield scrapy.Request(next_page)

	def parse_second(self, response):
		#获取产品的title, pic, specific, description
		title = response.css('h1::text').get().strip()
		title = re.sub('[\/:*?#”<>|]', '-', title)
		picture = response.css('span.img-thumb-item img::attr(src)').getall()
		picture_url = [i.replace('.jpg_50x50', '') for i in picture]
		data = response.css('ul.product-property-list').xpath('string(.)').get()
		data1 = re.sub(' ', '', data)
		data2 = re.sub(':\n', ':',data1)
		data2 = data2.strip()
		specifics = re.sub('\n+', '\n', data2)
		desc = response.css('script[type="text/javascript"]').getall()[3]
		decription_url = re.findall('detailDesc="(.*)"', desc)[0]
		dload = AliItem()
		dload['category'] = response.meta['category']
		dload['title'] = title
		dload['specifics'] = specifics
		dload['file_urls'] = decription_url
		dload['image_urls'] = picture_url
		return dload


class Getproxy(scrapy.Spider):
	name = 'proxy'
	start_page = 1
	max_page = 2
	base_url = 'https://www.xicidaili.com/nn/%s'
	start_urls = [base_url%start_page,]

	def parse(self, response):
		infos = response.xpath('//table[@id="ip_list"]/tr[position() > 1]')[:50]

		for info in infos:
			ip = info.xpath('.//td[2]/text()').get()
			port = info.xpath('.//td[3]/text()').get()
			ttype = info.xpath('.//td[6]/text()').get().lower()
			url = 'https://www.baidu.com'
			proxy = '%s://%s:%s'%(ttype, ip, port)
			meta = {
				'proxy': proxy,
				'dont_retry': True,
				'download_timeout': 10,
				'_proxy_ttype': ttype,
			}
			yield scrapy.Request(url, callback=self.check, meta=meta, dont_filter=True)
		if self.start_page < self.max_page:
			self.start_page += 1
		next_page = self.base_url%self.start_page
		yield response.follow(next_page)

	def check(self, response):
		if response:
			yield {'scheme': response.meta['_proxy_ttype'],
				'proxy': response.meta['proxy'],}
