from Util.Log import Log
from Util.Const import Const

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from Database.Database import Database
import pymongo
from datetime import datetime
import json
ALGO_VERSION = "0.1"
class Trust(MappedClass):
	""" Raw Features of an article """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_{0:s}'.format(ALGO_VERSION)
		indexes = [["id", "param_version"]]

	_id			= FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	param_version  		= FieldProperty(schema.Int)
	score		        = FieldProperty(schema.Float)
	sentiment_score		= FieldProperty(schema.Float)
	complexity_score	= FieldProperty(schema.Float)

	def toJSON(self):
		record = {"id":			  self.id,
			  "param_version":	  self.param_version,
			  "score":	          self.score,
			  "sentiment_score":	  self.sentiment_score,
			  "complexity_score":	  self.complexity_score
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return TrustArticle(id			   = record["id"],
				    param_version	   = record["param_version"],
				    score       	   = record["score"],
				    sentiment_score	   = record["sentiment_score"],
				    complexity_score	   = record["complexity_score"]
				    )

	@classmethod
	def get(cls, id):
		return cls.query.find({'id': id}).all()

	@classmethod
	def flush(cls):
		Database.flush()




    
