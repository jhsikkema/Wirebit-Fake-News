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
	sentiment_score		= FieldProperty(schema.String)
	complexity_punctuation	= FieldProperty(schema.String)
	complexity_wordlength	= FieldProperty(schema.String)
	complexity_duplication	= FieldProperty(schema.String)
	complexity_complexity	= FieldProperty(schema.String)
	article_length		= FieldProperty(schema.String)




	def toJSON(self):
		record = {"version":			    self.version,
			  "platform":			    self.platform,
k			  "publisher":			    self.publisher,
			  "sentiment_score":		    json.loads(self.sentiment_score),
			  "complexity_punctuation":	    json.loads(self.complexity_punctuation),
			  "complexity_wordlength":	    json.loads(self.complexity_wordlength),
			  "complexity_duplication":	    json.loads(self.complexity_duplication),
			  "complexity_complexity":	    json.loads(self.complexity_complexity),
			  "article_length":		    json.loads(self.article_length)
		}
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return TrustParameters(version		      = record["version"],
				       platform		      = record["platform"],
				       publisher	      = record["publisher"],
				       sentiment_score	      = json.dumps(self.sentiment_score),
				       complexity_punctuation = json.dumps(self.complexity_punctuation),
				       complexity_wordlength  = json.dumps(self.complexity_wordlength),
				       complexity_duplication = json.dumps(self.complexity_duplication),
				       complexity_complexity  = json.dumps(self.complexity_complexity),
				       article_length	      = json.dumps(self.article_length)
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




    
