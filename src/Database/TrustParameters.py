from Util.Log import Log
from Util.Const import Const

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from Database.Database import Database
import pymongo
from datetime import datetime
import json

class TrustParameters(MappedClass):
	""" Raw Features of an article """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_parameters'
		indexes = [["version"]]

	_id			= FieldProperty(schema.ObjectId)
	
	version			= FieldProperty(schema.Int)
	platform		= FieldProperty(schema.String)
	publisher		= FieldProperty(schema.String)
	sentiment_score_ci	= FieldProperty(schema.Float)
	lexical_complexity_ci	= FieldProperty(schema.Float)

	def toJSON(self):
		record = {"version":		   self.version,
			  "platform":		   self.platform,
			  "publisher":		   self.publisher,
			  "sentiment_score_ci":	   self.sentiment_score_ci,
			  "lexical_complexity_ci": self.lexical_complexity_ci
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return TrustArticle(version		   = record["version"],
				    platform		   = record["platform"],
				    publisher		   = record["publisher"],
				    sentiment_score_ci	   = record["sentiment_score_ci"],
				    lexical_complexity_ci   = record["lexical_complexity_ci"]
				    )

	@classmethod
	def getVersion(cls):
		record = cls.query.find().order({"version": pymongo.DESCENDING}).first()
		return record["version"]
		
	
	@classmethod
	def get(cls, version):
		return cls.query.find({"version": version}).all()
	
	@classmethod
	def flush(cls):
		Database.flush()




    
