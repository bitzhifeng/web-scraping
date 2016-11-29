#-*- coding: utf-8 -*-
import re
from common import download
import pdb

def crawler_sitemap(url):
	#download the sitemap file
	sitemap = download(url)
	#pdb.set_trace()
	#extract the sitemap links
	links = re.findall('<loc>(.*?)</loc>', sitemap)
	#download each link
	for link in links:
		html = download(link)
		#scrape html here
		#...

if __name__ == '__main__':
	crawler_sitemap('http://example.webscraping.com/sitemap.xml')
