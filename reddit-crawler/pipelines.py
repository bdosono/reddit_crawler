# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import json

from scrapy.contrib.exporter import JsonLinesItemExporter
from reddit_crawler.items import CommentItem, ThreadItem

class JsonExportPipeline(object):

	def __init__(self):
		self.file = open('tmp/export.json', 'w+b')

	def open_spider(self, spider):
		self.exporter = JsonLinesItemExporter(self.file)
		self.exporter.start_exporting()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()
