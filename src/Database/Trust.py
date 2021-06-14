from Util.Log import Log
from Util.Const import Const

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from Database.Database import Database
import pymongo
from datetime import datetime
import json
import re

ALGO_VERSION = "0.1"
class Trust(MappedClass):
	""" Raw Features of an article """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_{0:s}'.format(re.sub("[.]", "_", ALGO_VERSION))
		indexes = [["id", "param_version"]]

	_id			= FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	param_version		= FieldProperty(schema.Int)
	trust_score		= FieldProperty(schema.Float)
	inconsistency_score	= FieldProperty(schema.Float)
	sentiment_score		= FieldProperty(schema.Float)
	layout_score		= FieldProperty(schema.Float)
	complexity_score	= FieldProperty(schema.Float)
	platform_score		= FieldProperty(schema.Float)
	author_score		= FieldProperty(schema.Float)
	reasons			= FieldProperty(schema.String)

	def toJSON(self):
		record = {"id":			  self.id,
			  "param_version":	  self.param_version,
			  "trust_score":	  self.trust_score,
			  "sentiment_score":	  self.sentiment_score,
			  "inconsistency_score":  self.inconsistency_score,
			  "layout_score":	  self.layout_score,
			  "complexity_score":	  self.complexity_score,
			  "platform_score":	  self.platform_score,
			  "author_score":	  self.author_score,
			  "reasons":		  self.reasons,
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return Trust(id			   = record["id"],
			     param_version	   = record["param_version"],
			     score		   = record["score"],
			     sentiment_score	   = record["sentiment_score"],
			     inconsistency_score   = record["inconsistency_score"],
			     layout_score	   = record["layout_score"],
			     complexity_score	   = record["complexity_score"],
			     platform_score	   = record["platform_score"],
			     author_score	   = record["author_score"],
			     reasons		   = record["reasons"]
		)


	@classmethod
	def clean(cls):
		version = TrustParameters.getVersion()
		cls.query.remove({"param_version": {"$lt": version}})
	
	@classmethod
	def get(cls, id):
		return cls.query.find({'id': id}).sort([["param_version", pymongo.DESCENDING]]).first()

	@classmethod
	def flush(cls):
		Database.flush()




    
