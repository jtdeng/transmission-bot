#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this module implement the periodic tasks

import feed
from transmission import TransmissionClient

def periodic_task(xmpp, settings):
	'''this is the function that tranmission bot need to run periodically
	xmpp: the TransmissionBot instance, use to send messages
	settings: the global settings'''
	
	# xmpp.send_message(  mto='jtdeng@gmail.com',
 #                        mtype='chat',
 #                        mbody='hello',
 #                        mhtml='''<a href="http://www.google.co.jp">hello</a>''')

	dynamics = settings.dynamics
	logger = settings.logger

	logger.info('periodic task starting...')
	# check if there are new feed items and put them to queue
	for _id, fd in dynamics['feeds'].items():
		if fd['status'] == 'disabled':
			continue

		finfo, fdoc = feed.fetch_feed(fd['url'], fd['etag'], fd['modified'])
		logger.info('feed info: ' + str(finfo))
		if len(fdoc.entries)==0:
			logger.info('[%s] has no items'%(fd['title']))
			#print '%s has no items'%(fd['title'])
		else:
			#find new items
			new_items = feed.discover(fdoc, feed.decode_time(fd['last_published']))
			if len(new_items) == 0:
				logger.info('[%s] has no new items since %s'%(fd['title'], fd['last_published']))
				#print '%s has no new items since %s'%(fd['title'], fd['last_published'])
			else:
				#update queue in dynamics
				maxid = 0
				if not dynamics.has_key('queue'):
					dynamics['queue'] = {}
				elif dynamics['queue'].keys():
					maxid = max([int(x) for x in dynamics['queue'].keys()])	

				msg = 'I got something new for you in the queue\n'
				htmlmsg = '<p>I got something new for you in the queue<br>'
				for item in new_items:
					maxid += 1
					dynamics['queue'][str(maxid)] = {	'title':item['title'],
										 	  			'torrent_uri':item['torrent_uri'],
										 	  			'link':item['link'],
										 	  			'published':item['published'] }
					msg += '''%(title)s\n'''%item
					htmlmsg += '''<a href="%(link)s">%(title)s</a><br>'''%item
				htmlmsg += '</p>'
				logger.info(msg)
				# notify users with the new items
				if dynamics.get('notify', 'off') == 'on':
					for u in settings.accept_command_from:
						#print msg
						#print htmlmsg
						xmpp.send_message(  mto=u,
					 						mtype='chat',
					  						mbody=msg)
					   						#mhtml=htmlmsg )

				#new items found, so update the last_published to latest
				fd['last_published'] = feed.encode_time(finfo['last_published'])
				logger.info('Feed(%s) [%s]: update last_published to %s' % (_id, fd['title'], feed.encode_time(finfo['last_published'])))
		#whatever there are new items or not, update these info
		fd['title'] = finfo['title']
		fd['etag'] = finfo['etag']
		fd['modified'] = finfo['modified']
		#commit the change
		dynamics.sync()

	# notify completed downloads 
	torrents = TransmissionClient.list()
	if dynamics.get('downloads') == None:
		dynamics['downloads'] = {}
	# cleanup the downloads which do not exist 
	hslist = [x.hashString for x in torrents.values()]
	for hs in dynamics['downloads'].keys():
		if hs not in hslist:
			del dynamics['downloads'][hs]
			
	if dynamics.get('notify','off') == 'on':
		for _id, to in torrents.items():
			if to.progress < 100:
					dynamics['downloads'][to.hashString] = {'id':_id, 'name':to.name, 'progress':to.progress, 'status':to.status}
			else:
				if to.hashString in dynamics['downloads'].keys():
					for u in settings.accept_command_from:
						msg = '%s downloaded'%to.name
						xmpp.send_message(  mto=u,
				 							mtype='chat',
				  							mbody=msg )
					del dynamics['downloads'][to.hashString]

	dynamics.sync()

	# autostop the completed torrents
	if dynamics.get('autostop', 'off') == 'on':
		for _id, to in torrents.items():
			if to.progress >= 100:
				TransmissionClient.stop(_id)
			
	#ok, brb
	return True
