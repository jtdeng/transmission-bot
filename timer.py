#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this module implements the class for a periodic execution thread

import threading
from functools import wraps
import time
from settings import logger
import traceback

class PeriodicTimer(threading.Thread):
	def __init__(self, interval, callback, *args, **kwargs):
		threading.Thread.__init__(self)
		self.interval = interval
		self.callback = callback
		self.args = args
		self.kwargs = kwargs
		self.quit = False
		
	def run(self):
		while not self.quit:
			try:
				cont = self.callback(*self.args, **self.kwargs)
				self.quit = not cont
				time.sleep(self.interval)
			except:
				exc = traceback.format_exc()
				logger.warning(exc)
	
	def cancel(self):
		self.quit = True
		self.join()



if __name__ == '__main__':
	def say_hello(name, country='China'):
		print name, country
		return True
	
	t = PeriodicTimer(3, say_hello, 'James', country='China')	
	t.start()
	time.sleep(10)
	t.cancel()
