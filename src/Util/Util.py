"""
	Copyright Sikkema Software 2017. 
	No liabilities or rights can be derived from the correct working of 
	this software or.
"""
from Util.Const import Const
import os, os.path
from datetime import datetime, timedelta

class Util(object):
	
	@staticmethod
	def verify(condition, message):
		if not(condition):
			Log.info(message)
			exit(0)

