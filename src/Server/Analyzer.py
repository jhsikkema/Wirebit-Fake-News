import os, os.path
import re
import time
import glob
import dateutil.parser
import codecs
import json
import threading
import hashlib
from collections import deque
from IPFS.ipfs import IPFSGateway
from datetime import datetime, timedelta

from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
import argparse

from Database.Article import Article
from Database.Request import Request
from Database.Database import Database

class Analyzer(threading.Thread):
	INSTANCE = None
	def __init__(self, config):
		self.m_config		      = config
		self.m_run		      = False
		self.m_ipfs_gateway	      = IPFSGateway(self.m_config)
		self.m_settings		      = BlockSettings.get()
		self.m_queue		      = deque()

	@classmethod
	def get(cls, config):
		if not(self.INSTANCE):
			self.INSTANCE		      = Analyzer(config)
		return self.INSTANCE
				
	def run(self):
		while self.m_run:
			queue = Request.getQueue()
			for item in queue:
				pass
			time.sleep(1)

	def start(self):
		if (self.m_run):
			return
		self.m_run = True
		super(Analyzer, self).start()

	def stop(self):
		self.m_run = False


        def analyze(self):
                pass
                
	def validate(self, article_hash):
		articles = PublishedArticle.getArticleByHASH(article_hash)
		if len(articles) == 0:
			return ErrorCodes.VALIDATE_ARTICLE_NOT_RECOGNIZED
		article		   = articles[0]
		msg		   = ErrorCodes.VALIDATE_ARTICLE_SUCCESS
		block		   = article.toJSON()
		block['ipfs_hash'] = article.article
		block['id']	   = article.article
		block['url']	   = self.m_config[Const.STORAGE_BLOCK_EXPLORER_URL].format(**block)
		block['ipfs_url_local'] = "http://localhost:5001/api/v0/cat?arg={0:s}".format(str(article_hash))
		block['ipfs_url_global'] = "https://ipfs.io/ipfs/{0:s}".format(str(article_hash))
		msg['message'] = block
		return msg




if __name__=='__main__':
	parser = argparse.ArgumentParser(description="Run stand alone block explorer")
	parser.add_argument("--load-historic",	     help="Load historic data from file", action="store_true")
	parser.add_argument("--export-historic",     help="Export historic data from file", default="")
	parser.add_argument("--reload-transactions", help="Force loading older transactions", action="store_true")
	args = parser.parse_args()

	os.environ['FLASK_ENV'] = 'development'

	with Config(Const.CONFIG_PATH) as config:
		log = Log(config)
		analyzer = Analyzer(config)
		analyzer.start()
		analyzer.join()
		analyzer.stop()
				


