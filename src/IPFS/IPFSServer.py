import os, os.path
import time
from collections import deque
import threading
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from Database.Article import Article
from IPFS.ipfs import IPFSGateway
from IPFS.IPFSConst import IPFSConst
from IPFS.ArticleIndex import ArticleIndex
from IPFS.IPFSChannel import HashChannel, IndexChannel, PeerChannel
from IPFS.LocalArticles import LocalArticles


class IPFSServer(threading.Thread):
	def __init__(self, config, read_only=True):
		super(IPFSServer, self).__init__()
		self.m_ipfs_gateway    = IPFSGateway(config)
		self.m_config	       = config
		self.m_run		   = True
		self.m_read_only       = read_only
		self.m_ipfs_path       = os.path.join(self.m_config[IPFSConst.IPFS_PATH], self.m_config[IPFSConst.IPFS_OUTPUT])
		self.m_article_index   = ArticleIndex(self.m_config)
		self.m_local_articles  = LocalArticles(self.m_config)
		self.m_channels	       = {	'hash':	 HashChannel(self.m_config, self.m_ipfs_gateway),
									'index': IndexChannel(self.m_config, self.m_ipfs_gateway),
									'peer':	 PeerChannel(self.m_config, self.m_ipfs_gateway)}

		self.m_lock		   = threading.Condition()
		self.m_send_queue      = deque()
		self.m_sequence_nr     = 0

	def run(self):
		self.m_article_index.start()
		while(self.m_run):
			if self.m_read_only:
				if not(len(self.m_send_queue)):
					with self.m_lock:
						self.m_lock.wait()
					continue
				
			for i in range(1):
				for j in range(10):
					if not(len(self.m_send_queue)):
						with self.m_lock:
							self.m_lock.wait(timeout=60)
						continue
					time.sleep(0.1)

					with self.m_lock:
						article = self.m_send_queue.popleft()
					self.m_channels['hash'].send(article.ipfs_hash)
				
				for channel in self.m_channels.values():
					channel.checkMessages()
					for j in range(10):
						if not(channel.hasMessages()):
							break
						channel.receive()
				self.m_channels['peer'].ping()
			for channel in self.m_channels.values():
				channel.checkChannelID()
			if (not(self.m_read_only)):
				self.m_channels['index'].send()
			self.m_article_index.flush()
			self.m_channels['peer'].flush()
			self.m_channels['peer'].send()

	def __in__(self, article):
		return article in self.m_local_articles

	def get(self, article):
		return self.m_local_articles.get(article)
		
	def add(self, article):
		stored_articles = Article.getArticlesByContentHash(article)
		if stored_articles:
			Log.info("IPFS - stored_article", stored_articles)
			if (len(stored_articles) > 1):
				Log.info("Cleaning Article")
				Article.clean_one(article)
			stored_articles = [item for item in stored_articles if not(item.ipfs_hash == "")]
			Log.info("Nr IPFS HASHES", len(stored_articles))
			ipfs_hash	= stored_articles[0].ipfs_hash if len(stored_articles) else ""
			Log.info("IPFS HASH - ", ipfs_hash)
			if not(ipfs_hash == ""):
				return {'ipfs_hash': ipfs_hash, 'publish': False}
			else:
				ipfs_hash	  = self.m_article_index.add(article)
				Log.info("Published", ipfs_hash)
				article.ipfs_hash = ipfs_hash
				article.flush()
				return {'ipfs_hash': article.ipfs_hash, 'publish': False}
		ipfs_hash	  = self.m_article_index.add(article)
		Log.info(ipfs_hash)
		article.ipfs_hash = ipfs_hash
		article.flush()
		Log.info('IPFSServer - add before lock', article.ipfs_hash)
		with self.m_lock:
			self.m_send_queue.append(article)
			self.m_lock.notify_all()
		return {'ipfs_hash': article.ipfs_hash, 'publish': True}

	def stop(self):
		self.m_run = False
		self.m_article_index.stop()


if __name__=="__main__":
	with Config(Const.CONFIG_PATH) as config:
		log = Log(config)
		server = IPFSServer(config, config[IPFSConst.CONFIG_READ_ONLY_SERVER].lower() == 'false')
		server.start()
		server.join()
		server.stop()
