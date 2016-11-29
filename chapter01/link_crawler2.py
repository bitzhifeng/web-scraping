#-*- coding: utf-8 -*-

import re
import urlparse
from common import download
import pdb

def link_crawler(seed_url, link_regex):
	"""
	Crawler from the given seed URL following links matched by link_regex
	"""
	crawl_queue = [seed_url]
	pdb.set_trace()
	seen = set(crawl_queue) #keep trace which URL's have seen before
	while crawl_queue:
		url = crawl_queue.pop()
		html = download(url)
		for link in get_links(html):
			# check if link matches expected regex
			if re.match(link_regex, link):
				# form absolute link
				link = urlparse.urljoin(seed_url, link)
				#check if have already seen this link
				if link not in seen:
					seen.add(link)
					crawl_queue.append(link)

def get_links(html):
	"""
	Return a list of links from html
	"""
	# a regular expression to extract all links from the webpage
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	#list of all links from webpage
	return webpage_regex.findall(html)

if __name__ == '__main__':
	link_crawler('http://example.webscraping.com', '/(index|view)')