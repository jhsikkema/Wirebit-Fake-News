"""
	Copyright Sikkema Software 2017. 
	No liabilities or rights can be derived from the correct working of 
	this software or.
"""
from Util.Const import Const
from Util.CSVFile import CSVFile
import os, os.path
import codecs
import re
from datetime import datetime

# Class to connect to email server and send error reports 
class Frequencies(object):
	def __init__(self, config, path):
		self.m_config 		= config
		self.m_frequencies 	= {}
		self.m_path 		= path
		
	def view(self, id):
		now = datetime.now().strftime('%Y%m%d-%H%M%S')
		if not id in self.m_frequencies:
			self.m_frequencies[id] = {}
			self.m_frequencies[id]['frequency'] = 0
			self.m_frequencies[id]['last_viewed'] = ""
		self.m_frequencies[id]['frequency'] += 1
		self.m_frequencies[id]['last_viewed'] = now

	def key_by_frequency(self):
		data = [[key, value['frequency']] for (key, value) in self.m_frequencies.items()] 
		return [line[0] for line in sorted(data, key=lambda x: x[1], reverse=True)]
		
	def key_by_last_viewed(self):
		data = [[key, value['last_viewed']] for (key, value) in self.m_frequencies.items()] 
		return [line[0] for line in sorted(data, key=lambda x: x[1], reverse=True)]
	
			
	def __enter__(self):
		print(self.m_config)
		print(self.m_path)
		print(Const.CSV_SEPARATOR)
		print(self.m_config[Const.OUTPUT_CSV_SEPARATOR])
		with CSVFile(self.m_path, 'r', self.m_config[Const.OUTPUT_CSV_SEPARATOR]) as infile:
			print(infile.header)
			assert infile.header == ['id', 'frequency', 'last_viewed'], "Util.Frequencies - Invalid header for storage file. Required {0:s}".format(self.m_config[Const.OUTPUT_CSV_SEPARATOR].join(['id', 'frequency', 'last_viewed']))

			for item in infile:
				self.m_frequencies[item['id']] = {}
				self.m_frequencies[item['id']]['frequency']  = int(item['frequency'])
				self.m_frequencies[item['id']]['last_viewed']  = item['last_viewed']
		return self
		
	def __exit__(self, type, value, trace):
		with CSVFile(self.m_path, 'w', self.m_config[Const.OUTPUT_CSV_SEPARATOR]) as outfile:
			outfile.header = ['id', 'frequency', 'last_viewed']
			for (key, value) in self.m_frequencies.items():
				item = {}
				item['id'] = key
				item['frequency'] = str(value['frequency'])
				item['last_viewed'] = value['last_viewed']
				outfile.write(item)
				
			
		
	def reset(self):
		for key in self.m_frequencies.keys():
			self.m_frequencies[key]['frequency'] = 0
			self.m_frequencies[key]['last_viewed'] = ""
			
		
