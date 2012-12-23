#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file defines all the settings needed by transmission-bot

import logging
from logging.handlers import RotatingFileHandler
import sys
import jsonshelve

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
					'file': 'transmission-bot.log'
				 }

logger = create_logger()

# XMPP account for the bot, keep it top secret
xmpp_username = ''
xmpp_password = ''

# a whitelist of XMPP contacts that are allowed to send commands to bot
accept_command_from = []

# if your bot must use a proxy to connect, configure it here
# also applies to other internet connections except connection to transmission rpc
use_proxy = False 
proxy_config = { 'host': '', 
                 'port': 8080, 
                 'username':None, 
                 'password':None }

# transmission rpc server 
# if you enabled access control on transmission, put the RPC user/pass here
transmission_rpc_config = { 'address': 'localhost',
							'port': 9091,
							'user': None,
							'password': None }

# dynamic configurations are saved in this file as json document
dynamic_config = 'dynamic.json'
dynamics = jsonshelve.open(dynamic_config)					


# the interval in seconds between each run of the periodic task which checks feeds,
# autostop downloads and notify on completion
task_interval = 60