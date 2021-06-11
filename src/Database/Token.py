import os, os.path

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
import pymongo
import hashlib
from datetime import datetime
import json
import re
import hashlib, binascii

from Util.Log import Log
from Util.Const import Const
from Database.Database import Database


class RevokedToken(MappedClass):
	class __mongometa__:
		session = Database.getInstance()
		name	= 'revoked_token'
		indexes = [["jti"]]

	_id	    = FieldProperty(schema.ObjectId)
	jti	    = FieldProperty(schema.String(required=True))
	
	def toJSON(self):
		record = {"jti":		  self.jti
			  }
		return record

	@classmethod
	def fromJSON(self, record):
		return RevokedToken(jti	 = record["jti"])

	@classmethod
	def flush(cls):
		db = Database.getInstance()
		db.flush()




    
