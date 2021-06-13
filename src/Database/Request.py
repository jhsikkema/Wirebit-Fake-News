from Util.Log import Log
from Util.Const import Const

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from Database.Database import Database
import pymongo
import hashlib
from collections import deque
from datetime import datetime
import json
import re

class Request(MappedClass):
	class __mongometa__:
		session = Database.getInstance()
		name	= 'request'
		indexes = [["id"], ["processing", "timestamp"]]

	_id			= FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	timestamp		= FieldProperty(schema.DateTime)
	processing		= FieldProperty(schema.Bool)

	def toJSON(self):
		record = {"id":			  self.id,
			  "timestamp":		  self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
			  "processing":		  self.processing
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(cls, record):
		timestamp = record["timestamp"]
		if isinstance(timestamp, str):
			timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
		record["processing"] = record["processing"] if "processing" in record else False
		return Request(	 id	   = record["id"],
				 timestamp   = timestamp,
				 processing  = record["processing"]
			       )


	@classmethod
	def getQueue(cls):
		return deque([item for item in cls.query.find({'processing': False}).sort([["timestamp",  pymongo.ASCENDING]]).limit(100)])


	@classmethod
	def flush(cls):
		db = Database.getInstance()
		db.flush()

