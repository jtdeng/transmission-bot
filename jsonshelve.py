#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A python shelve like class, but persist to json file

import os
import json
import UserDict
import time 

# class StructTimeEncoder(json.JSONEncoder):
# 	'''JSON encoder for time.struct_time'''
# 	def default(self, obj):
# 		if isinstance(obj, time.struct_time):
# 			return time.strftime('%Y-%m-%d %H:%M:%S', obj)
# 		return json.JSONEncoder.default(self, obj)


# def time_hookdecode(self, str):
# 		print str
# 		return time.strptime(str, '%Y-%m-%d %H:%M:%S')


class JsonShelve(UserDict.DictMixin):
	'''load a json file and use it like a python dict'''
	def __init__(self, fname):
		self.fname = fname
		self.jsondict = {}
		# track if any change performed on the memory jsondict
		self.out_of_sync = False

		#if persistent file does't exit, create it
		if not os.path.exists(fname):
			self.sync(force=True)
		else: #load the json file to memory
			with file(fname, 'r') as fp:
				self.update(json.load(fp))

	def keys(self):
		return self.jsondict.keys()

	def __len__(self):
		return len(self.jsondict)
 
	def has_key(self, key):
		return key in self.jsondict

	def __contains__(self, key):
		return key in self.jsondict
   
	def get(self, key, default=None):
		if key in self.jsondict:
			return self[key]
		return default
   
	def __getitem__(self, key):
		return self.jsondict[key]
   
	def __setitem__(self, key, value):
		self.jsondict[key] = value
		self.out_of_sync = True
   
	def __delitem__(self, key):
		del self.jsondict[key]
		self.out_of_sync = True
   
	def close(self):
		self.sync()
		self.jsondict = None
   
	def sync(self, force=False):
		if not (self.out_of_sync or force):
			return

		with file(self.fname, 'w') as fp:
			json.dump(self.jsondict, fp, sort_keys=True, indent=4, separators=(',', ': '))

    # extra extended methods
	def loads(self, str):
		'''load the json string to this object, without sync to disk'''
		self.update(json.loads(str))
		self.out_of_sync = True

	def dumps(self):
		'''dump this object to json string'''
		return json.dumps(self.jsondict, sort_keys=True, indent=4, separators=(',', ': '))


def open(filename):
	return JsonShelve(filename)

if __name__ == '__main__':
	js = open('test.json')
	js['name'] = 'James'
	js['country'] = 'China'
	js['favorites'] = {'sports':['swimming', 'hiking'], 'music':['jazz','blues']} 
	print js.dumps()
	js.loads('{"country": "China", "name": "James", "favorites": {"sports": ["swimming", "hiking"]}}')	
	print js.dumps()
	for k,v in js.get('favorites', {}).items():
		print k,v
	sports = js['favorites']['sports']
	sports.append('running')	
	js.close()
