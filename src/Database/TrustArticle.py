from Util.Log import Log
from Util.Const import Const

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from Database.Database import Database
import pymongo
from datetime import datetime
import json

class TrustArticle(MappedClass):
	""" Raw Features of an article """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_articles'
		indexes = [["id"], ["sentiment_score", "platform", "publisher"], ["lexical_complexity", "platform", "publisher"]]

	_id			= FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	platform		= FieldProperty(schema.String)
	publisher		= FieldProperty(schema.String)
	sentiment		= FieldProperty(schema.Float)
	sentiment_anger		= FieldProperty(schema.Float)
	sentiment_joy		= FieldProperty(schema.Float)
	sentiment_score		= FieldProperty(schema.Float)
	lexical_complexity	= FieldProperty(schema.Float)

	def toJSON(self):
		record = {"id":			  self.id,
			  "platform":		  self.platform,
			  "publisher":		  self.publisher,
			  "sentiment":		  self.sentiment,
			  "sentiment_anger":	  self.sentiment_anger,
			  "sentiment_joy":	  self.sentiment_joy,
			  "sentiment_score":	  self.sentiment_score,
			  "lexical_complexity":	  self.lexical_complexity
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return TrustArticle(id			   = record["id"],
				    platform		   = record["platform"],
				    publisher		   = record["publisher"],
				    sentiment		   = record["sentiment"],
				    sentiment_anger	   = record["sentiment_anger"],
				    sentiment_joy	   = record["sentiment_joy"],
				    sentiment_score	   = record["sentiment_score"],
				    lexical_complexity	   = record["lexical_complexity"]
				    )

	@classmethod
	def get(cls, id):
		return cls.query.find({'id': id}).all()

	@classmethod
	def flush(cls):
		Database.flush()




    
