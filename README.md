# reddit-crawler
A scrapy project for collecting comment threads from subreddits, developed for social network analysis (SNA) and qualitative coding purposes.

### Command-Line Arguments
##### -a subreddit=NAME
Specifies a subreddit to crawl. NAME is a string containing the name of the subreddit (e.g., https://reddit.com/r/python would be -a subreddit=python). There is no default subreddit to scrape so this argument is required.
##### -a pages=NUMBER
Specifies the number of pages to scrape (not the number of threads or the crawl depth).
