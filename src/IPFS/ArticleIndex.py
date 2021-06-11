import json
import time
from datetime import datetime, timedelta
import threading
from collections import deque

from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from IPFS.ipfs import IPFSGateway
from IPFS.PostArticle import PostArticle
from Database.Article import Article


class DayIndex(object):
	def __init__(self, date_str, config, ipfs_gateway):
		self.m_date	 = date_str
		self.m_config	 = config
		self.m_ipfs_gateway = ipfs_gateway
		self.m_file_path = "/bywire/indices/article_index_{0:s}".format(self.m_date)
		self.m_data_path = "/bywire/data/{0:s}".format(self.m_date)
		self.m_header	 = ";".join(["hash", "id", "title", "author", "preview", "revision", "timestamp"])
		self.m_index	 = {}
		self.m_articles	 = []
		self.m_counter	 = 0
		self.m_changed	 = False
		self.setup(None)
	
	def setup(self, response, **kwargs):
		Log.info('Setup', str(response))
		if (response is None):
			Log.info(self.m_file_path)
			self.m_ipfs_gateway.exists(self.m_file_path, self.setup)
		elif (response.status_code == 500):
			Log.info("Setup - Storing Document")
			Log.info(self.m_data_path)
			self.m_ipfs_gateway.createDir(self.m_data_path)
			self.m_ipfs_gateway.storeDocument(self.m_file_path, self.m_header, self.parseAnswer)
		elif (response.status_code == 200):
			content = json.loads(response.content)
			Log.info('Content', content)

	@staticmethod
	def parseAnswer(result, **kwargs):
		Log.info('printAnswer')
		Log.info(result)
		Log.info(result.status_code)
		Log.info(result.content)
		if (result.status_code == 200):
			data = json.loads(result.content)

	def storeHash(self, result, article, **kwargs):
		Log.info('storeHash')
		Log.info(result)
		Log.info(result.status_code)
		Log.info(result.content)
		if (result.status_code == 200):
			data = json.loads(result.content)
			Log.info('Data', data)
			Log.info("Hash" in data)
			if "Hash" in data:
				Log.info(len(self.m_articles))
				Log.info(data["Hash"])
				article.ipfs_hash = data["Hash"]
				article.flush()
				Log.info(data["Hash"])
				self.m_index[article.ipfs_hash] = article
				self.m_articles[article_id] = article
				Log.info(article.ipfs_hash)
		elif (result.status_code == 500):
			Log.error('File not properly uploaded')
			Log.error(result.content)

	def flush(self):
		if not(self.m_changed):
			return
		content = self.m_header+"\n"+"\n".join([article.toIndexCSV() for article in self.m_articles])
		#self.m_ipfs_gateway.storeDocument(self.m_file_path, content, self.parseAnswer)
		self.m_ipfs_gateway.storeDocument(self.m_file_path, content, self.storeHash)
		self.m_changed = False

	def article_path(self, article):
		return self.m_data_path + '/' + article.filename()


	def publish(self, article):
		path = self.article_path(article)

		Log.info('ArticleIndex - add', path)
		Log.info('ArticleIndex - add', json.dumps(article.toJSON()))

		self.m_counter += 1
		self.m_articles.append(article)
		location = len(self.m_articles)-1
		self.m_ipfs_gateway.storeDocument(path, json.dumps(article.toJSON()), lambda x, **kwargs: self.storeHash(x, article, **kwargs))
		self.m_changed = True
		return location
		
	def write(self):
		self.m_ipfs_gateway.updateDocument(self.m_file_path, self.m_header)

	def read(self):
		pass

	def mergeCallback(self, result):
		Log.info(result)
		
	def merge(self, remote_hash):
		Log.info('Merge', remote_hash)
		self.m_ipfs_gateway.retrieveDocumentFromHash(remote_hash, self.mergeCallback)


class ArticleIndex(threading.Thread):
	def __init__(self, config):
		super(ArticleIndex, self).__init__()
		self.m_ipfs_gateway = IPFSGateway(config)
		self.m_config	    = config
		self.m_lock	    = threading.Lock()
		self.m_run	    = True
		self.m_queue	    = deque()
		self.m_index	    = {}


	def run(self):
		last_check = datetime.now()-timedelta(hours=2)
		while (self.m_run):
			article = None
			with self.m_lock:
				if len(self.m_queue):
					article = self.m_queue.pop()
			if not article is None:
				pass
			else:
				time.sleep(1)
			if datetime.now() - last_check > timedelta(hours=1):
				self.findUnpublished()
				last_check = datetime.now()
			time.sleep(0.01)

	def stop(self):
		self.m_run = False

	def findUnpublished(self):
		unpublished = Article.getNotInIPFS()
		for article in unpublished:
			duplicates = Article.getArticlesByContentHash(article)
			duplicates = [item for item in duplicates if not(item.ipfs_hash == "")]
			if len(duplicates):
				article.ipfs_hash = duplicates[0].ipfs_hash
				article.flush()
				continue
			with self.m_lock:
				self.m_queue.append(article)

	def getIndex(self, article):
		today = article.pubdate.strftime('%Y%m%d')
		if not today in self.m_index:
			self.m_index[today] = DayIndex(today, self.m_config, self.m_ipfs_gateway)
		return self.m_index[today]

	def publish(self, article):
		index	 = self.getIndex(article)
		index.publish(article)

	def add(self, article):
		with self.m_lock:
			self.m_queue.append(article)
		index = self.getIndex(article)
		Log.info('ArticleIndex - PostArticle', article.author, article.publisher);
		if not(article.author in ('bywiretoken', 'bywirewriter')):			  
			Log.info('ArticleIndex - PostArticle');
			post = PostArticle(self.m_config)
			post.send(article)
			Log.info('ArticleIndex - store - added')
		return self.m_ipfs_gateway.getHash(index.article_path(article), article.toJSON())

	def flush(self):
		for article in self.m_index.values():
			article.flush()


if __name__=="__main__":
	with Config(Const.CONFIG_PATH) as config:
		index = ArticleIndex(config)
		article = Article()
		index.add(article)
