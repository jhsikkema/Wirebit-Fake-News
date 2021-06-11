from Util.Log import Log
from IPFS.IPFSConst import IPFSConst
import threading
from Database.Article import Article
from datetime import datetime, timedelta

class LocalArticles(threading.Thread):
	CACHE_LENGTH = 1000
	CACHE_CLEAN_FREQUENCY = 3600
	def __init__(self, config):
		self.m_config	  = config
		self.m_cache	  = {}
		articles = Article.getArticlesByDate(datetime.now().date())
		for article in articles:
			self.m_cache[article.id] = {'article': article, 'count': 0}
		CACHE_LENGTH = int(self.m_config[IPFSConst.CACHE_LENGTH])
		CACHE_CLEAN_FREQUENCY = int(self.m_config[IPFSConst.CACHE_CLEAN_FREQUENCY])
		self.m_last_clean = datetime.now()

		
	def get(self, article_id):
		Log.info("LocalArticles.get - Getting article", article_id)
		if article_id in self.m_cache:
			self.m_cache[article_id]['count'] += 1
			return self.m_cache[article_id]['article']
		found = Article.getArticleByHASH(article_id)
		if found:
			self.m_cache[article_id] = {'article': found[0], 'count': 1}
			return found[0]
		return None


	def __in__(self, article):
		return not(self.get(article) is None)

	def clean(self):
		if len(self.m_cache) < LocalArticles.CACHE_LENGTH:
			return
		if datetime.now() - self.m_last_clean < timedelta(seconds=LocalArticles.CACHE_CLEAN_FREQUENCY):
			return
		while len(self.m_cache) >= LocalArticles.CACHE_LENGTH:
			minimum = min([item['count'] for item in self.m_cache])
			self.m_cache = dict([(key, value) for (key, value) in self.m_cache.items if value['count'] > minimum])
		return 
