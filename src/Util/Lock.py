"""
	Copyright Sikkema Software 2017. 
	No liabilities or rights can be derived from the correct working of 
	this software or.
"""
from Util.Const import Const
import os, os.path
from datetime import datetime, timedelta

class Lock(object):
	ENTER = '0'
	EXIT  = '1'
	NOW_FCT = lambda obj: datetime.now()
	
	def __init__(self, config):
		self.m_path = config[Const.LOCK_FILE]
		self.m_timeout   = config[Const.LOCK_TIMEOUT]
		self.m_timeout   = [int(item) for item in self.m_timeout.split(':')]
		self.m_timeout   = timedelta(hours=self.m_timeout[0], minutes=self.m_timeout[1], seconds=self.m_timeout[2])
		self.m_separator = config[Const.LOCK_SEPARATOR]
		self.m_format    = config[Const.LOCK_FORMAT]
		
	def __enter__(self):
		self.m_re_entrant = False
		now = self.NOW_FCT()
		if (os.path.exists(self.m_path)):
			with open(self.m_path, 'r') as infile:
				data = [line.split(self.m_separator) for line in infile if line.strip()]
				if len(data):
					last_entry = datetime.strptime(data[-1][0], self.m_format)
					self.m_re_entrant = (data[-1][1]==self.ENTER and (now-last_entry) < self.m_timeout)
				data = [ line[0]+self.m_separator+line[1].strip() for line in data if now-datetime.strptime(line[0], self.m_format) < timedelta(days=7)]
			with open(self.m_path, 'w') as outfile:
				outfile.write("\n".join(data)+"\n")
			if not(self.m_re_entrant):
				if (Lock.ENTER):
					with open(self.m_path, 'w') as infile:
						infile.write(now.strftime(self.m_format)+self.m_separator+Lock.ENTER+"\n")
		else:
			if (Lock.ENTER):
				with open(self.m_path, 'w') as infile:
					infile.write(now.strftime(self.m_format)+self.m_separator+Lock.ENTER+"\n")
		return self
		
	def __exit__(self, type, value, traceback):
		if not(self.m_re_entrant):
			now = self.NOW_FCT()
			if (Lock.EXIT):
				with open(self.m_path, 'r') as infile:
					data = [line.split(self.m_separator) for line in infile if line.strip()]
					data[-1][1] = Lock.EXIT
				with open(self.m_path, 'w') as outfile:
					for item in data:
						outfile.write(item[0]+self.m_separator+item[1].strip()+"\n")
			
			
