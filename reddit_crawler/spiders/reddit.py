# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request
from scrapy.selector import Selector

from reddit_crawler.items import ThreadItem, CommentItem

class RedditSpider(scrapy.Spider):
	name = "reddit"
	allowed_domains = ["reddit.com"]

	def __init__(self, subreddit=None, pages=None, *args, **kwargs):
		super(RedditSpider, self).__init__(*args, **kwargs)
		self.start_urls = ['https://www.reddit.com/r/%s/new/' % subreddit]
		self.pages = int(pages)
		self.page_count = 0

	def parse(self, response):
		self.log("MAIN PAGE LINK: %s" % response.url)
		sel = Selector(response)
		threads = sel.xpath("//div[@id='siteTable']/div[@onclick]")
		next_page = sel.xpath("//div[@id='siteTable']/div[@class='nav-buttons']/span/a[@rel='nofollow next']/@href").extract()
		
		for thread in threads:
			item = ThreadItem()
			item['threadID'] = thread.xpath("@data-fullname").extract()
			item['title'] = thread.xpath("div[@class='entry unvoted']/p[@class='title']/a/text()").extract()
			item['link'] = thread.xpath("div[@class='entry unvoted']/p[@class='title']/a/@href").extract()
			item['score'] = thread.xpath("div[@class='midcol unvoted']/div[@class='score unvoted']/text()").extract()
			item['post_date'] = thread.xpath("div[@class='entry unvoted']/p[@class='tagline']/time/@title").extract()
			item['user'] = thread.xpath("div[@class='entry unvoted']/p[@class='tagline']/a/@href").extract()
			item['comment_url'] = thread.xpath("div[@class='entry unvoted']/ul/li/a/@href").extract()

		 	request = Request(item['comment_url'][0], callback=self.parse_thread)
			request.meta['item'] = item
			
			yield request
			
		if (self.pages > 1) and (self.page_count < self.pages):
			self.page_count += 1
			request = Request(next_page[0], callback=self.parse)
			yield request
		
	def parse_thread(self, response):
		self.log("THREAD PAGE LINK: %s" % response.url)
		sel = Selector(response)
		comments = sel.xpath("//div[@role='main']/div[@class='commentarea']/div[@class='sitetable nestedlisting']//div[@data-fullname]")
		comment_items = []
		thread = response.meta['item']
	
		for comment in comments:
			item = CommentItem()
			
			if (comment.xpath("../@class").extract()[0] == "sitetable listing"):	# check for a parent comment
				item['parent'] = comment.xpath("../@id").re('[a-zA-Z0-9]*$')[0]		# if parent comment exists, get the parent's commentID from the @id tag
			else:
				item['parent'] = []													# else set value to an empty list
			
			item['commentID'] = comment.xpath("p[@class='parent']/a/@name").extract()
			item['user'] = comment.xpath("div[@class='entry unvoted']/p/a[2]/@href").extract()
			item['post_date'] = comment.xpath("div[@class='entry unvoted']/p/time/@title").extract()
			item['score'] = comment.xpath("div[@class='entry unvoted']/p/span[@class='score unvoted']/text()").extract()
			item['text'] = comment.xpath("div[@class='entry unvoted']/form/div/div").extract()
			
			comment_items.append(item)

		thread['comments'] = comment_items		

		yield thread
