# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib.request import urlretrieve
import requests
from os.path import join
import os

class AliPipeline(object):
	#specific文本存储
	def process_item(self, item, spider):
		path = spider.settings.get('FILES_STORE')
		path1 = path + join(item['category'], item['title'], 'specific.txt')
		tpath = path + join(item['category'], item['title'])
		if os.path.exists(tpath):
			pass
		else:
			os.makedirs(tpath)
		with open(path1, 'w') as f:
			f.write(item['specifics'])
			f.close()
		return item


class MyFilesPipeline(object):
	#description网页存储
	def process_item(self, item, spider):
		path = spider.settings.get('FILES_STORE')
		path1 = path + join(item['category'], item['title'], 'decription.html')
		fpath = path + join(item['category'], item['title'])
		
		if os.path.exists(fpath):
			pass
		else:
			os.makedirs(fpath)
		res = requests.get(item['file_urls'])
		data = res.content
		with open(path1, 'wb') as f:
			f.write(data)
			f.close()
		return item


class MyimagesPipeline(object):
	#图片存储
	def process_item(self, item, spider):
		path = spider.settings.get('FILES_STORE')
		path1 = path + join(item['category'], item['title'])
		images = item['image_urls']
		for i in range(len(images)):
			ipath = path1 + '\\%s.jpg'%i
			urlretrieve(images[i], ipath)
		return item

class MyproxyPipeline(object):
	def process_item(self, item, spider):
		return item