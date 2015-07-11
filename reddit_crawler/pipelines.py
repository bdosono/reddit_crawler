# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import json
import psycopg2
import psycopg2.extensions
import re

# register typecasters to receive all db input in unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

from scrapy.contrib.exporter import JsonLinesItemExporter
from reddit_crawler.items import CommentItem, ThreadItem

class JsonExportPipeline(object):

	def __init__(self):
		self.file = open('data/export.json', 'w+b')

	def open_spider(self, spider):
		self.exporter = JsonLinesItemExporter(self.file)
		self.exporter.start_exporting()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()

class PostgresExportPipeline(object):

	def __init__(self):
		# IMPORTANT: to work, must replace values with the name, user, and password for the database
                self.conn = psycopg2.connect(database="NAME", user="USER", password="PASSWORD")
                self.cur = self.conn.cursor()
		self.cur.execute("LOCK TABLE threads IN SHARE ROW EXCLUSIVE MODE;")
		self.cur.execute("LOCK TABLE comments IN SHARE ROW EXCLUSIVE MODE;")
	
	def process_item(self, item, spider):
		if isinstance(item, ThreadItem):
			threadID = item['threadID'][0]
			title = item['title'][0]
			link = item['link'][0]
			datetime = self.format_datetime(item['post_date'][0])
			score = self.format_score(item['score'][0])
			username = item['user'][0]
			threadurl = item['comment_url'][0]
			try:
				body = item['text'][0]	# if thread is a self post, the self post text goes here
			except:
				body = ""		# otherwise, set value to empty string

			sql = """WITH upsert AS (UPDATE threads SET body = %s, score = %s, datetime = %s WHERE threadID = %s RETURNING *) 
				INSERT INTO threads (threadID, title, link, datetime, score, username, threadurl, body) 
				SELECT %s, %s, %s, %s, %s, %s, %s, %s
				WHERE NOT EXISTS (SELECT * FROM upsert);"""

			data = (body, score, datetime, threadID, threadID, title, link, datetime, score, username, threadurl, body, )

			self.cur.execute(sql, data)
		
			for comment in item['comments']:
				try:
					threadID = item['threadID'][0]	# comments use the threadID of the ThreadItem it is contained in
					commentID = comment['commentID'][0]
					body = comment['text'][0]
					username = comment['user'][0]
					parent = comment['parent']	# comment['parent'] is a string, not a list (see: reddit.parse_thread)
					datetime = self.format_datetime(comment['post_date'][0])
	
					if comment['score'] == []:	# if comment['score'] is an empty list
						score = "NA"		# set score to NA
					else:
						score = self.format_score(comment['score'][0])
	
					sql = """WITH upsert AS (UPDATE comments SET body = %s, score = %s, datetime = %s WHERE commentID = %s RETURNING *)
						INSERT INTO comments (threadID, commentID, body, username, parent, datetime, score) 
						SELECT %s, %s, %s, %s, %s, %s, %s
						WHERE NOT EXISTS (SELECT * FROM upsert);"""
	
					data = (body, score, datetime, commentID, threadID, commentID, body, username, parent, datetime, score, )
	
					self.cur.execute(sql, data)
				except:
					pass
	
			self.conn.commit()
		return item

	def close_spider(self, spider):
		self.cur.close()
		self.conn.close()

	def format_score(self, s):
		p = re.compile('[-]?\d*')
		r = p.search(s)		# searches string and returns match object
		result = r.group(0)	# assigns first subgroup of search() to result
		return result

	def format_datetime(self, s):
		"""
		Returns a formatted string containing the date and time to pass to the postgresql database.
		Input ex. : Fri Jun 12 22:40:18 2015 UTC
		Output ex.: 2015-06-12 22:40:18
		"""
		p = re.compile(r'\s+')
		dt_list = p.split(s)	# splits scraped timestamp by whitespace and assigns result to dt_list
		year = dt_list[4]
		m_dict = {"Jan": "1", "Feb": "2", "Mar": "3", "Apr": "4", "May": "5", "Jun": "6", "Jul": "7", "Aug": "8", "Sep": "9", "Oct": "10", "Nov": "11", "Dec": "12"}
		month = m_dict[dt_list[1]]
		day = dt_list[2]
		time = dt_list[3]
		datetime = year + "-" + month + "-" + day + " " + time
		return datetime
