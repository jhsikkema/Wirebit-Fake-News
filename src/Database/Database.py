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
