#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this module implement the feed parsing

import feedparser
import urllib2
import settings
from pprint import pprint
import time

def decode_time(str):
	'''decode time from string'''
	try:
		t = time.strptime(str, '%Y-%m-%d %H:%M:%S')
		return t
	except:
		return None

def encode_time(tm):
	'''encode time to string'''
	try:
		str = time.strftime('%Y-%m-%d %H:%M:%S', tm)
		return str
	except:
		return None

def fetch_feed(url, etag=None, modified=None):
	'''fetch the feed content, returns feed info and feed content'''
	handlers = []
	if settings.use_proxy:
		http_proxy = settings.proxy_config['host'] + ":" + str(settings.proxy_config['port'])
		proxy_handler = urllib2.ProxyHandler( {"http":http_proxy} )
		handlers.append(proxy_handler)
		if settings.proxy_config['username']:
			proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
			proxy_auth_handler.add_password(None, None, settings.proxy_config['username'], 
														settings.proxy_config['password'])
			handlers.append(proxy_auth_handler)
			
	f = feedparser.parse(url, handlers=handlers, etag=etag, modified=modified)
	
	if len(f.entries) == 0:
		last_published = None
	else:
		last_published = f.entries[0]['published_parsed']

	info = {'etag': f.get('etag', None),
			'modified': f.get('modified', None),
			#'updated': encode_time(f.feed.updated_parsed),
			'last_published': last_published,
			'title': f.feed.title}
	return info, f

	
def discover(feed, last_published):
	'''discover the new items since last published from fetched feed'''
	new_items = []
	for e in feed.entries:
		#print '%s was published at %s, last_published=%s' % (e['title'], encode_time(e['published_parsed']), encode_time(last_published))
		if last_published == None or encode_time(e['published_parsed']) > encode_time(last_published):
			torrent_uri = e.get('magneturi', e.get('download', e['link']))
			new_items.append({'title': e['title'],
							  'torrent_uri': torrent_uri,
							  'link': e['id'],
							  'published': encode_time(e['published_parsed']) })
		else:
			break # since entries are ordered by published, don't have to read on

	return new_items


if __name__ == '__main__':
	info, f = fetch_feed('http://www.bestxl.com/rss.php')
	#f = fetch_feed('http://rss.thepiratebay.se/207')
	pprint(info)
	import time
	pprint(discover(f, time.strptime('Sun Dec 02 00:00:00 2012')))
	
	
	
