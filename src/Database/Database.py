"""

	Copyright Sikkema Software B.V. 2021 - All rights Reserved

	You may not copy, reproduce, distribute, modify or create 
	derivative works sell or offer it for sale or use such content
	to construct any kind of database or disclose the source without
	explicit permission of the copyright holder. You may not alter
	or remove any copyright or other notices from copies of the content. 
	For permission to use the content please contact sikkemasoftware@gmailcom

	All content and data is provided on an as is basis. The copyright holder
	makes no claisms to the accuracy, complentness, currentness, suistainability
	or validity of the code and information and will not be liable for any
	errors, omissions, or delays in this information or any losses, injuries
	or damages arising from the use of this software. 

"""


import sys
import os, os.path

from Database.DBConst import DBConst

from Util.Config import Config
from Util.Const import Const

from ming import create_datastore
from ming.odm import ThreadLocalODMSession

class Database(object):
	__INSTANCE = None
	# Wrapper around Mondodb.
    
	def __init__(self, config):
		assert Database.__INSTANCE is None, "Database.__init__ - Init called twice access through getInstance"
		self.m_url	= config[DBConst.DATABASE_URL]
		self.m_port		= config[DBConst.DATABASE_PORT]
		self.m_schema		= config[DBConst.DATABASE_SCHEMA]
		print(self.m_url, self.m_port, self.m_schema)
		self.m_datastore	= create_datastore("mongodb://{0:s}:{1:s}/{2:s}".format(self.m_url, self.m_port, self.m_schema))
		self.m_session		= ThreadLocalODMSession(bind=self.m_datastore)
		Database.__INSTANCE	= self


	@classmethod
	def getInstance(cls):
		if not(Database.__INSTANCE):
			print("Creating Database", Const.CONFIG_PATH)
			with Config(Const.CONFIG_PATH) as config:
				db = Database(config)
		return Database.__INSTANCE.m_session

	@classmethod
	def flush(cls):
		db = Database.getInstance()
		db.flush()

if __name__ == "__main__":
	sys.path.append(os.path.join(os.getcwd(), ".."))
	print("Setting up database...")
	with Config(Const.CONFIG_PATH) as config:
		instance = Database.getInstance()
