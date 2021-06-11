"""
	Copyright Sikkema Software 2017. 
	No liabilities or rights can be derived from the correct working of 
	this software or.
"""
from Util.Const import Const
import os, os.path
import codecs
import re

# Class to connect to email server and send error reports 
class Settings(object):
	ENCODING = 'utf-8'

	def __init__(self, path):
		self.m_path	 = path
		self.m_settings	 = {}
		self.read()

	def read(self):
		if not(os.path.exists(self.m_path)):
			self.m_settings = {}
			return
		with codecs.open(self.m_path, 'r', encoding=Settings.ENCODING) as infile:
			self.m_settings = dict([[value.strip() for value in item.split('=')] for item in infile if item.count('=')])
			self.m_settings['last_timestamp'] = int(self.m_settings['last_timestamp']) if'last_timestamp' in self.m_settings else 0
		return 

	def write(self):
		backup_path = self.m_path+".bak"
		with codecs.open(backup_path, 'w', encoding=Settings.ENCODING) as outfile:
			outfile.write("\n".join(["{0: <30s} = {1: <30s}".format(key, str(value)) for (key, value) in self.m_settings.items()]))
		os.replace(backup_path, self.m_path)

	def flush(self):
		self.write()
		self.read()

	def __getitem__(self, key):
		return self.m_settings[key] if key in self.m_settings else None
	
	def __setitem__(self, key, value):
		self.m_settings[key] = value
	
