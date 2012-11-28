#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file defines all the settings needed by transmission-bot

import logging
from logging.handlers import RotatingFileHandler
import sys

# a handy function to create a logger using defined settings
def create_logger():
	# Set up a specific logger with our desired output level
	logging.basicConfig(level=logging_config['level'],
						format=logging_config['format'],
						filename=logging_config['file'],
						)
	my_logger = logging.getLogger()
	return my_logger


###########################################################################
### Settings start from here 
###########################################################################

# logging for the bot, follow python logging
logging_config = {	'level': logging.DEBUG,
					'format': '[%(asctime)-15s]  %(levelname)-8s <%(filename)s:%(lineno)d> - %(message)s',
					'file': '/var/tmp/transmission-bot.log'
				 }

logger = create_logger()

# XMPP account for the bot
xmpp_username = ''
xmpp_password = ''

# a whitelist of XMPP contacts that are allowed to send commands to bot
accept_command_from = []

# proxy settings
use_proxy = False
proxy_config = { 'host': '', 
                 'port': 8080, 
                 'username':None, 
                 'password':None }

# transmission rpc server, usually you won't change it
transmission_rpc_config = { 'address': 'localhost',
							'port': 9091,
							'user': None,
							'password': None }

						
