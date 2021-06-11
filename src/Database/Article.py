from Util.Log import Log
from Util.Const import Const

from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from Database.Database import Database
import pymongo
import hashlib
from datetime import datetime
import json
import re

class Article(MappedClass):
	class __mongometa__:
		session = Database.getInstance()
		name	= 'articles'
		indexes = [["id"], ["publisher", "id"], ["author", "id"]]

	_id			    = FieldProperty(schema.ObjectId)
	
	id			= FieldProperty(schema.String(required=True))
	author			= FieldProperty(schema.String)
	publisher		= FieldProperty(schema.String)
	platform		= FieldProperty(schema.String)
	title			= FieldProperty(schema.String)
	has_senntiment		= FieldProperty(schema.Boolean)
	content			= FieldProperty(schema.String(required=True))
	content_hash		= FieldProperty(schema.String)
	timestamp		= FieldProperty(schema.DateTime)

	@classmethod
	def fromIPFS(cls):
		return id.startswith("IPFS_")
	
	def toJSON(self):
		record = {"id":			  self.id,
			  "author":		  self.author,
			  "publisher":		  self.publisher,
			  "platform":		  self.platform,
			  "title":		  self.title,
			  "content":		  self.content,
			  "content_hash":	  self.content_hash,
			  "ipfs_hash":		  self.ipfs_hash,
			  "timestamp":		  self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
		}
		return record

	def __str__(self):
		return str(self.toJSON())

	@staticmethod
	def genID(content_hash, ipfs_hash):
		return content_hash if not(ipfs_hash) else "IPFS_"+ipfs_hash

	@classmethod
	def fromJSON(self, record):
		Log.info("Article.fromJSON", record)
		record["timestamp"] = record["timestamp"]  if "timestamp" in record else datetime.now()
		timestamp = record["timestamp"]
		
		if isinstance(timestamp, str):
			timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
		if not("content_hash" in record):
			record["content_hash"] = Article.contentHash(record)
		if not("ipfs_hash" in record):
			record["ipfs_hash"] = ""
                if not("id" in record):
                        record["id"] = Article.genID(record["content_hash"], record["ipfs_hash"])
		return Article(id	     = record["id"],
			       author	     = record["author"],
			       publisher     = record["publisher"],
			       platform	     = record["platform"],
			       title	     = record["title"],
			       content	     = record["content"],
			       timestamp     = record["timestamp"],
			       content_hash  = record["content_hash"],
			       ipfs_hash     = record["ipfs_hash"],
		)

	@staticmethod
	def contentHash(record):
		content = record["title"]+record["author"]+record["content"]
		return str(hashlib.sha512(bytes(content, 'utf-8')).hexdigest().encode('ascii'))

	@classmethod
	def getArticle(cls, id):
		return cls.query.find({'id': id}).first()

	@classmethod
	def fromMessage(cls, message):
		data	 = message
		timestamp=datetime.now()
		record = {"id":		     data[Const.REQ_ARTICLE],
			  "content":	     data[Const.REQ_ARTICLE_CONTENT] if Const.REQ_ARTICLE_CONTENT in data else "",
			  "timestamp":	     timestamp,
			  "title":	     data[Const.REQ_ARTICLE_TITLE],
			  "author":	     data[Const.REQ_ARTICLE_AUTHOR],
			  "publisher":	     data["publisher"],
			  "platform":	     data["platform"]}
		article = cls.fromJSON(record)
		return article

	@classmethod
	def flush(cls):
		db = Database.getInstance()
		db.flush()




    
