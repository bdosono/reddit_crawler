# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThreadItem(scrapy.Item):
	"""
	Represents a post on the subreddit.
	
	ThreadItem['comments'] contains CommentItem objects.
	"""
	threadID = scrapy.Field()
	title = scrapy.Field()
	link = scrapy.Field()
	post_date = scrapy.Field()
	score = scrapy.Field()
	user = scrapy.Field()
	comment_url = scrapy.Field()
	text = scrapy.Field()
	comments = scrapy.Field()

class CommentItem(scrapy.Item):
	"""
	Represents an individual comment associated with a thread.
	"""
	commentID = scrapy.Field()
	parent = scrapy.Field()
	user = scrapy.Field()
	post_date = scrapy.Field()
	score = scrapy.Field()
	text = scrapy.Field()
