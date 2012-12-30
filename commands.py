#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file implements all the commands

import sys
import shlex
from inspect import getmembers, isfunction
import time

from transmission import TransmissionClient
import jsonshelve
import feed
import settings
from settings import dynamics

__module__ = sys.modules[globals()['__name__']]

def sort_as_int(lst):
	'''sort a list of numeric string as integer'''
	int_lst = [int(x) for x in lst if x.isdigit()]
	int_lst.sort()
	return [str(x) for x in int_lst]

# execute the input command string, and dispatch to each command class
def execute(cmdargs):
	cmd = shlex.split(cmdargs)
	if len(cmd)==0:
		return "Type $help to get all commands"

	cmd_funcs = [f[1] for f in getmembers(__module__) if isfunction(f[1]) and (f[0]=='cmd_'+cmd[0].lower())]
	
	if cmd_funcs:
		return cmd_funcs[0](*cmd[1:])
	else:
		return "Hey buddy, I can't understand it: " + cmd[0]


def cmd_help(*args):
	'''show the usage of all commands
....$help [command]'''

	if len(args) >= 1:
		funcs = [f for f in getmembers(__module__) if isfunction(f[1]) and f[0]==('cmd_'+args[0]).lower()]
		if len(funcs) == 1:
			fn,fv = funcs[0]
			resp = '$%s: %s\n' % (fn[4:], fv.__doc__)
		else:
			resp = 'Sorry, no such command: ' + args[0]
	else:
		resp = '''My lord, this is all I can serve you\n\n'''
		funcs = [f for f in getmembers(__module__) if isfunction(f[1]) and f[0].startswith('cmd_')]	
		for fn,fv in funcs:
			resp += '$%s: %s\n' % (fn[4:], fv.__doc__)
	
	return resp


def cmd_status(*args):
	'''show the status of all torrents'''
	resp = 'ID  Status  Progress  Size  Name\n'
	torrents = TransmissionClient.list()
	tids = torrents.keys()
	tids.sort()
	tfiles = TransmissionClient.get_files(tids)
	
	disk_usage = 0.0
	for tid in tids:
		to = torrents[tid]
		total_size = sum([x['size'] for x in tfiles[tid].values()])/float(1024*1024*1024)
		disk_usage += (to.progress*total_size)/100
		resp += '%2d  %s  %.2f%%  %.2fG  %-s\n' % (tid, to.status, to.progress, total_size, to.name)
	
	resp += 'Total disk usage is %.2fG\n'%(disk_usage)
	return resp


def cmd_add(*args):
	"""add a new torrent to transmission
....$add url <torrent_url>
....$add base64 '<torrent_base64>'"""
	if len(args) != 2:
		return "Oops, wrong number of arguments, type $help for more"

	if args[0].lower() == 'url':
		TransmissionClient.add_uri(args[1])
		resp = 'Torrent added'
	elif args[0].lower() == 'base64':
		TransmissionClient.add(args[1])
		resp = 'Torrent added'
	else:
		return "'%s' is not a valid option, type $help for more" % args[0].lower()

	return resp


def cmd_start(*args):
	'''start downloading for torrent(s)
....$start <ids>|all'''
	if len(args) != 1:
		return "Oops, wrong number of arguments, type $help for more"

	if args[0].lower() == 'all':
		ids = [str(x) for x in TransmissionClient.list().keys()]	
	else:
		ids = args[0].split(',')

	TransmissionClient.start(ids)
	return 'Torrent ' + ','.join(sort_as_int(ids)) + ' started'
		

def cmd_stop(*args):
	'''stop downloading for torrent(s)
....$stop <ids>|all'''
	if len(args) != 1:
		return "Oops, wrong number of arguments, type $help for more"

	if args[0].lower() == 'all':
		ids = [str(x) for x in TransmissionClient.list().keys()]	
	else:
		ids = args[0].split(',')

	TransmissionClient.stop(ids)
	return 'Torrent ' + ','.join(sort_as_int(ids)) + ' stopped'


def cmd_remove(*args):
	'''remove torrent only or both torrent and data
....$remove <ids>|all [data]'''
	if len(args) not in [1,2]:
		return "Oops, wrong number of arguments, type $help for more"	
	
	resp = ''
	delete_data = False

	if args[0].lower() == 'all':
		ids = [str(x) for x in TransmissionClient.list().keys()]
	else:
		ids = args[0].split(',')

	if len(args)==2 and args[1].lower() == 'data':
		delete_data = True
		resp = 'Torrent ' + ','.join(sort_as_int(ids)) + ' removed with data'
	else:
		resp =  'Torrent ' + ','.join(sort_as_int(ids)) + ' removed'

	TransmissionClient.stop(ids)
	TransmissionClient.remove(ids, delete_data)
	return resp


def cmd_notify(*args):
	'''turn on/off notification on completion or feed updates
....$notify [on|off]'''
	if len(args) == 0:
		return 'Notify is ' + dynamics.get('notify', 'not set')
	elif len(args) == 1 and args[0].lower() in ['on', 'off']:
		dynamics['notify'] = args[0].lower()
		dynamics.sync()
		return "Notify has been turned " + args[0].lower()
	else:
		return "Oops, invalid arguments, type $help for more"
	

def cmd_autostop(*args):
	'''turn on/off automatic stop on completion
....$autostop [on|off]'''
	if len(args) == 0:
		return 'Autostop on completion is ' + dynamics.get('autostop', 'not set')
	elif len(args) == 1 and args[0].lower() in ['on', 'off']:
		dynamics['autostop'] = args[0].lower()
		dynamics.sync()
		return "Automatic stop on completion has been turned " + args[0].lower()
	else:
		return "Oops, invalid arguments, type $help for more"


def cmd_config(*args):
	"""manage dynamic configurations
....$config dump
....$config load '<json_string>'"""
	if len(args) not in [1,2]:
		return "Oops, wrong number of arguments, type $help for more"	

	if len(args) == 1 and args[0].lower() == 'dump':
		return dynamics.dumps()
	elif len(args) == 2 and args[0].lower() == 'load':
		try:
			dynamics.loads(args[1])
			dynamics.sync()
			return 'Configuration loaded successfully'
		except:
			return 'JSON format error'
	else:
		return "Invalid arguments, type $help for more"


def cmd_feed(*args):
	'''manage subscriptions of bittorrent feeds 	
....$feed list
....$feed subscribe <feed_url>
....$feed unsubscribe <ids>|all
....$feed enable|disable <ids>|all'''

	if len(args) not in [1,2]:
		return "Oops, wrong number of arguments, type $help for more"	

	resp = ''
	if len(args) == 1 and args[0].lower() == 'list':
		resp += 'ID  Status  Title  LastPublished  URL\n'
		if dynamics.get('feeds', {}) == {}:
			return 'No feeds yet'
		
		#when json loaded to dict, it's not sorted by key
		sorted_ids = [int(x) for x in dynamics['feeds'].keys()]
		sorted_ids.sort()
		for k in sorted_ids:
			v = dynamics['feeds'][str(k)]
			resp += "%s  %s  %s  %s  %s\n" %(k, v['status'], v['title'], v['last_published'], v['url'])
		
		return resp

	elif len(args) == 2 and args[0].lower() == 'subscribe':
		maxid = 0
		url = args[1]
		if not dynamics.has_key('feeds'):
			dynamics['feeds'] = {}
		elif dynamics['feeds'].keys():
			maxid = max([int(x) for x in dynamics['feeds'].keys()])	

		info, f = feed.fetch_feed(url)
		dynamics['feeds'][str(maxid+1)] = {	'title':info['title'],
											'status': 'enabled',
								 	  		'last_published': feed.encode_time(info['last_published']),
								 	  		'etag':info['etag'],
								 	  		'modified':info['modified'],
								 	  		'url':url }
		dynamics.sync()
		return "Feed '%s' subscribed successfully" % (info['title'])

	elif len(args) == 2 and args[0].lower() == 'unsubscribe':
		if dynamics.get('feeds', {}) == {}:
			return 'Feed list is empty'
				
		if args[1].lower() == 'all':
			ids_to_delete = dynamics['feeds'].keys()
		else:
			ids_to_delete = args[1].split(',')

		ids_deleted = []
		for _id in ids_to_delete:
			if dynamics['feeds'].has_key(_id):
				del dynamics['feeds'][_id]
				ids_deleted.append(_id)

		dynamics.sync()

		if ids_deleted:
			return "Feed %s unsubscribed" % (','.join(sort_as_int(ids_deleted)))
		else:
			return "Feed list is empty"
	elif len(args) == 2 and args[0].lower() in ('enable','disable'):
		stat = args[0].lower() + 'd'
		if dynamics.get('feeds', {}) == {}:
			return 'No feeds yet'
		if args[1].lower() == 'all':
			ids_to_op = dynamics['feeds'].keys()
		else:
			ids_to_op = args[1].split(',')

		ids_done = []
		for _id in ids_to_op:
			if dynamics['feeds'].has_key(_id):
				dynamics['feeds'][_id]['status'] = stat
				ids_done.append(_id)

		dynamics.sync()

		if ids_done:
			return "Feed %s %s" % (','.join(sort_as_int(ids_done)), stat)
		else:
			return "Feed list is empty"	
	else:
		return "Oops, invalid arguments, type $help for more"


def cmd_queue(*args):
	'''manage item queue discovered from subscribed feeds  	
....$queue list
....$queue download <ids>|all
....$queue remove <ids>|all'''

	if len(args) not in [1,2]:
		return "Oops, wrong number of arguments, type $help for more"	

	resp = ''
	if len(args) == 1 and args[0].lower() == 'list':
		resp += 'ID  Published  Title\n'
		if dynamics.get('queue', {}) == {}:
			return 'Queue is empty'
		
		#when json loaded to dict, it's not sorted by key
		sorted_ids = [int(x) for x in dynamics['queue'].keys()]
		sorted_ids.sort()
		for k in sorted_ids:
			v = dynamics['queue'][str(k)]
			resp += "%s  %-s  %-s\n" %(k, v['published'], v['title'])
		
		return resp

	elif len(args) == 2 and args[0].lower() == 'download':
		if dynamics.get('queue', {}) == {}:
			return 'Queue is empty'
				
		if args[1].lower() == 'all':
			ids_to_dl = dynamics['queue'].keys()
		else:
			ids_to_dl = args[1].split(',')

		ids_downloading = []
		for _id in ids_to_dl:
			if dynamics['queue'].has_key(_id):
				TransmissionClient.add_uri(dynamics['queue'][_id]['torrent_uri'])
				ids_downloading.append(_id)
				del dynamics['queue'][_id]

		dynamics.sync()

		if ids_downloading:
			return "Started downloading item %s" % (','.join(sort_as_int(ids_downloading)))
		else:
			return "No download started"

	elif len(args) == 2 and args[0].lower() == 'remove':
		if dynamics.get('queue', {}) == {}:
			return 'Queue is empty'
				
		if args[1].lower() == 'all':
			ids_to_rm = dynamics['queue'].keys()
		else:
			ids_to_rm = args[1].split(',')

		ids_removed = []
		for _id in ids_to_rm:
			if dynamics['queue'].has_key(_id):
				ids_removed.append(_id)
				del dynamics['queue'][_id]

		dynamics.sync()

		if ids_removed:
			return "Removed item %s" % (','.join(sort_as_int(ids_removed)))
		else:
			return "No item removed"

	else:
		return "Oops, invalid arguments, type $help for more"
