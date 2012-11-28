#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import shlex
from inspect import getmembers, isfunction

from transmission import TransmissionClient


__module__ = sys.modules[globals()['__name__']]

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
	'''show the usage of all supported commands'''
	resp = '''My lord, this is all I can serve you\n'''
	for fn,fv in [f for f in getmembers(__module__) if isfunction(f[1]) and f[0].startswith('cmd_')]:
		resp += '$%s: %s\n' % (fn[4:], fv.__doc__)
	
	return resp

def cmd_status(*args):
	'''display the status of all torrents'''
	resp = 'ID  Status          Progress(%)  Name\n'
	torrents = TransmissionClient.list()
	for tid,to in torrents.items():
		resp += '%2d  %-14s  %-11.2f  %-s\n' % (tid, to.status, to.progress, to.name)
	#print resp
	return resp

def cmd_add(*args):
	'''add a new torrent
	$add url <torrent_url>
	$add base64 <torrent_base64>'''
	if len(args) != 2:
		return "Not enough arguments, type $help for more"

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
	$start [ <ids> | all ]'''
	if len(args) != 1:
		return "Not enough arguments, type $help for more"

	if args[0].lower() == 'all':
		ids = [str(x) for x in TransmissionClient.list().keys()]	
	else:
		ids = args[0].split(',')

	TransmissionClient.start(ids)
	return 'Torrent ' + ','.join(ids) + ' started'
		

def cmd_stop(*args):
	'''stop downloading for torrent(s)
	$stop [ <ids> | all ]'''
	if len(args) != 1:
		return "Not enough arguments, type $help for more"

	if args[0].lower() == 'all':
		ids = [str(x) for x in TransmissionClient.list().keys()]	
	else:
		ids = args[0].split(',')

	TransmissionClient.stop(ids)
	return 'Torrent ' + ','.join(ids) + ' stopped'


def cmd_remove(*args):
	'''remove torrent(s)
	$remove [ <ids> | all ] [ torrent | data ] '''
	if len(args) != 2:
		return "Not enough arguments, type $help for more"	
	resp = ''
	if args[0].lower() == 'all':
		ids = [str(x) for x in TransmissionClient.list().keys()]
	else:
		ids = args[0].split(',')

	if args[1].lower() == 'data':
		delete_data = True
		resp = 'Torrent ' + ','.join(ids) + ' removed with data'
	elif args[1].lower() == 'torrent':
		delete_data = False
		resp = 'Torrent ' + ','.join(ids) + ' removed'
	else:
		return "'%s' is not a valid option, type $help for more" % args[1].lower()

	TransmissionClient.stop(ids)
	TransmissionClient.remove(ids, delete_data)
	return resp
