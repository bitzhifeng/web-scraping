# -*- coding: utf-8 -*-

import re
from common import download
import pdb
def link_crawler(seed_url, link_regex):
	"""
	Crawl from the given seed URL following links mathched by link_regex
	"""
	craw_queue = [seed_url] # the queue of URL's to download
	while craw_queue:
		url = craw_queue.pop()
		html = download(url)
		pdb.set_trace()
		# filter for links matching our regular expression
		for link in get_links(html):
			if re.match(link_regex, link):
				# add this link to the crawl queue
				craw_queue.append(link)

def get_links(html):
	"""
	Return a list of links from html
	"""
	# a regular expression to extract all links from the webpage
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', 
		re.IGNORECASE)
	return webpage_regex.findall(html)

if __name__ == '__main__':
	link_crawler('http://example.webscraping.com', '/(index|view)')

