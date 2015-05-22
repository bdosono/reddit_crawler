# reddit_crawler
A scrapy project for collecting comment threads from subreddits, developed for social network analysis and qualitative coding purposes.

### Command-Line Arguments
##### subreddit
Usage: -a subreddit=NAME
Specifies which subreddit to crawl. (e.g., https://reddit.com/r/python should be -a subreddit=python)
##### pages
Useage: -a pages=INT
The number of pages to crawl. Pages here refers to following 'next page' links on the nav bar, not the number of threads to scrape, links to follow generally, or the crawl depth. So, for example, if you wanted to go back 3 pages and scrape all the comment threads from them, you would use -a pages=3.
