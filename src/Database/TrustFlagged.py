from Util.Log import Log
from Util.Const import Const

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from Database.Database import Database
import pymongo
from datetime import datetime
import json

class TrustFlagged(MappedClass):
	""" Raw Features of an article """
	class __mongometa__:
		session = Database.getInstance()
		name = 'trust_flagged'
		indexes = [["id"]]

	_id			= FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	is_fake			= FieldProperty(schema.Bool)
	export_vote		= FieldProperty(schema.Int)
	reader_vote		= FieldProperty(schema.Int)

	def toJSON(self):
		record = {"id":			  self.id,
			  "is_fake":		  self.is_fake,
			  "export_vote":	  self.export_vote,
			  "reader_vote":	  self.reader_vote
			  }
		return record

	def __str__(self):
		return str(self.toJSON())
	
	@classmethod
	def fromJSON(self, record):
		return TrustArticle(id			   = record["id"],
				    is_fake		   = record["is_fake"]
				    expert_vote		   = record["export_vote"]
				    reader_vote		   = record["reader_vote"]
				    )

	@classmethod
	def get(cls, id):
		return cls.query.find({'id': id}).first()

	@classmethod
	def flush(cls):
		Database.flush()




    
