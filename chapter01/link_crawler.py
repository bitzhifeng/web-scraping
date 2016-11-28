#-*- coding: utf-8 -*-

import re
import urlparse
import urllib2
import time
from datetime import datetime
import robotparser
import Queue

def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, 
	headers=None, user_agent='wswp', proxy=None, num_retries=1):
	"""
	 Crawl from the given seed URL following links matched by the link_regex
	"""
	# the queue of URL's that still need to be crawled
	crawl_quque = Queue.deque([seed_url])
	# the URL's that have been seen and at what depth
	seen = {seed_url: 0}
	# trace how many URL's have been downloaded
	num_urls = 0
	rp = get_robots(seed_url)
	throttle = Throttle(delay)
	headers = headers or {}
	if user_agent:
		headers['User_agent'] = user_agent
	while crawl_quque:
		url = crawl_quque.pop()
		# check url passes robots.txt restrictions
		if rp.can_fetch(user_agent, url):
			throttle.wait(url)
			html = download(url, headers, proxy=proxy, num_retries=num_retries)
			links = []
			depth = seen[url]
			if depth != max_depth:
				# can still crawl further
				if link_regex:
					# filter for links matching our regular expression
					links.extend(link for link in get_links(html) if re.match(link_regex, link))
				for link in links:
					link = normalize(url, link)
					# check whether already crawled this link
					if link not in seen:
						seen[link] = depth + 1
						#check link in same domain
						if same_domain(seed_url, link):
							crawl_quque.add(link)
			num_urls += 1
			#check whether have reached the download maximum
			if num_urls == max_urls:
				break
		else:
			print 'Blocked by robots.txt:', url
	 


class Throttle:
	"""
	Throttle downloading by sleeping between the requests to  same domains
	"""
	def __init__(self, delay):
		# amount of delay between downloads for each domains
		self.delay = delay
		# timestamp of when a domain was the last accessed
		self.domains = {}

	def wait(self, url):
		domain = urlparse.urlparse(url).netloc
		last_accessed = self.domains.get(domain)
		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				time.sleep(sleep_secs)
		self.domains[domain] = datetime.now()

def download(url, headers, proxy, num_retries, data=None):
	print 'Downloading:', url
	request = urllib2.Request(url, data, headers)
	opener = urllib2.build_opener()
	if proxy:
		proxy_params = {urlparse.urlparse(url).schema: proxy}
		opener.add_handler(urllib2.ProxyHandler(proxy_params))
	try:
		html = opener.open(request).read()
	except urllib2.URLError as e:
		print 'Downloading errors:', e.reason
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				# Retry 5XX HTTP error
				html = download(url, headers, proxy, num_retries - 1, data)
	return html

def normalize(seed_url, link):
	"""
	normalize this URL by remvoing the hash and adding the domain
	"""
	link, _ = urlparse.urldefrag(link) # Remove the hash to avoid duplicates
	return urlparse.urljoin(seed_url, link)

def same_domain(url1, url2):
	"""
	Return True if both URL belong same domain
	"""
	return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc

def get_robots(url):
	"""
	 Initialize robots parser for this domain
	"""
	rp = robotparser.RobotFileParser
	rp.set_url(urlparse.urljoin(url, '/robots.txt'))
	rp.read()
	return rp

def get_links(html):
	"""
	Return a list of links fromthis html
	"""
	# A regular expression to extract the all links from the webpage
	webpage_regex = re.compile('<a[^>]+href=["\](.*?)["\]', re.INGNORECASE)
	#lists of all links from the webpage
	return webpage_regex.findall(html)

































