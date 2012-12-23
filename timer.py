#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this module implements the class for a periodic execution thread

import threading
from functools import wraps
import time
from settings import logger
import traceback

class PeriodicTimer(object):
	def __init__(self, interval, callback, *args, **kwargs):
		self.interval = interval
		self.args = args
		self.kwargs = kwargs
		
		#print args, kwargs
		@wraps(callback)
		def wrapper(*args, **kwargs):
			try:
				ok = callback(*args, **kwargs)
			except:
				exc = traceback.format_exc()
				logger.warning(exc)
				ok = True

			if ok:
				self.thread = threading.Timer(self.interval, self.callback, args, kwargs)
				self.thread.start()

		self.callback = wrapper

	def start(self):
		self.thread = threading.Timer(self.interval, self.callback, self.args, self.kwargs)
		self.thread.start()

	def cancel(self):
		self.thread.cancel()




if __name__ == '__main__':
	def say_hello(name, country='China'):
		print name, country
		return True
	
	t = PeriodicTimer(3, say_hello, 'James', country='China')	
	t.start()
	time.sleep(4)
	t.cancel()
