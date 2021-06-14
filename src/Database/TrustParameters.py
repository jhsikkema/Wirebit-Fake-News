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
	""" Maps Features of an article to the range [0-1] to allow better learning """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_parameters'
		indexes = [["version"]]

	_id			= FieldProperty(schema.ObjectId)
	
	version			= FieldProperty(schema.Int)
	platform		= FieldProperty(schema.String)
	publisher		= FieldProperty(schema.String)
	sentiment_score_cutoff	= FieldProperty(schema.Float)
	sentiment_score_scale	= FieldProperty(schema.Float)
	article_length_cutoff	= FieldProperty(schema.Float)
	article_length_scale	= FieldProperty(schema.Float)
	complexity_punctuation_cutoff	= FieldProperty(schema.Float)
	complexity_punctuation_scale	= FieldProperty(schema.Float)

	def toJSON(self):
		record = {"version":		    self.version,
			  "platform":		    self.platform,
			  "publisher":		    self.publisher,
			  "sentiment_score_cutoff": self.sentiment_score_cutoff,
			  "sentiment_score_cutoff": self.sentiment_score_scale,
			  "article_length_cutoff":  self.article_length_cutoff,
			  "article_length_scale":   self.article_length_scale,
			  "complexity_punctuation_cutoff":  self.complexity_punctuation_cutoff,
			  "complexity_punctuation_scale":   self.complexity_punctuation_scale
		}
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return TrustParameters(version		   = record["version"],
				       platform		   = record["platform"],
				       publisher		   = record["publisher"],
				       sentiment_score_cutoff = record["sentiment_score_cutoff"],
				       sentiment_score_scale  = record["sentiment_score_scale"],
				       article_length_cutoff  = record["article_length_cutoff"],
				       article_length_scale   = record["article_length_scale"],
				       complexity_punctuation_cutoff  = record["complexity_punctuation_cutoff"],
				       complexity_punctuation_scale   = record["complexity_punctuation_scale"]
				    )

	@classmethod
	def clean(cls):
		version = cls.getVersion()
		cls.query.remove({"version": {"$lt": version}})
		
	@classmethod
	def getVersion(cls):
		record = cls.query.find().sort([["version", pymongo.DESCENDING]]).first()
		return record["version"] if record else 0
		
	
	@classmethod
	def get(cls, version):
		return cls.query.find({"version": version}).all()
	
	@classmethod
	def flush(cls):
		Database.flush()




    
