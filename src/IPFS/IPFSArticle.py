from Util.Log import Log

class IPFSArticle(object):
	def __init__(self, hash_value="", title="", author="", content="", timestamp="", preview=""):
		self.m_hash	  = hash_value
		self.m_id	  = id
		self.m_title	  = title
		self.m_author	  = author
		self.m_content	  = content
		self.m_timestamp  = timestamp
		self.m_preview	  = preview
		self.m_revision	  = 0

	def filename(self):
		return "{0:s}.txt".format(str(self.m_id))

	def toJSON(self):
		Log.info('to_json')
		return {'hash': str(self.m_hash),
			'id': str(self.m_id),
			'title': str(self.m_title),
			'author': str(self.m_author),
			'timestamp': str(self.m_timestamp),
			'content': str(self.m_content),
			'preview': str(self.m_preview),
			'revision': str(self.m_revision)}

	@staticmethod
	def fromJSON(self, data):
		Log.info('from_json', data)
		article = Article()
		article.m_hash	= data['hash']
		article.m_id	= data['id']
		article.m_title = data['title']
		article.m_author = data['author']
		article.m_timestamp = data['timestamp']
		article.m_content = data['content']
		article.m_preview = data['preview']
		article.m_revision = data['revision']
		return article
		
	def toIndexCSV(self):
		return ";".join([self.m_hash, self.m_id, self.m_title, self.m_author, self.m_preview, str(self.m_revision), self.m_timestamp])
