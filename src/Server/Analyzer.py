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
from datetime import datetime, timedelta
import argparse
import math
import traceback

from nrclex import NRCLex
from nltk import corpus, tokenize, stem
from IPFS.ipfs import IPFSGateway
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from Database.Article import Article
from Database.Request import Request
from Database.Trust	      import Trust
from Database.TrustArticle    import TrustArticle
from Database.TrustParameters import TrustParameters
from Database.Database import Database
from IPFS.ipfs import IPFSGateway

# Import according to the docs didn't work on our server
#from expertai.client import ExpertAiClient
from expertai.nlapi.common.errors import ExpertAiRequestError as ExpertAiRequestError

class Analyzer(threading.Thread):
	""" Analyzer: Core class to calculate trust scores 
	"""
	INSTANCE = None
	def __init__(self, config):
		super(Analyzer, self).__init__()
		self.m_config		      = config
		self.m_ipfs_gateway	      = IPFSGateway(config)
		self.m_run		      = False
		self.m_queue		      = deque()
		self.m_parameters	      = [item for item in TrustParameters.get(TrustParameters.getVersion())]
		print("PARAMETERS")
		print(self.m_parameters)
		self.m_parameters	      = self.m_parameters[0] if self.m_parameters else None
		self.m_nlp_client	      = None
		if config[Const.EXPERTAI_USE].lower() == "true":
			os.environ["EAI_USERNAME"] = config[Const.EXPERTAI_USERNAME]
			os.environ["EAI_PASSWORD"] = config[Const.EXPERTAI_PASSWORD]
			self.m_nlp_client = ExpertAiClient()
			
		print(self.m_parameters)

		
	@classmethod
	def get(cls, config=None):
		print(cls.INSTANCE)
		if not(cls.INSTANCE):
			cls.INSTANCE		      = Analyzer(config)
		return cls.INSTANCE
				
	def run(self):
		while self.m_run:
			queue = Request.getQueue()
			for request in queue:
				request.processing = True
				article = Article.get(request.id)
				if not(article):
					if (request.fromIPFS()):
						self.download(request)
					else:
						Log.error("ERROR *** Article not found")
				else:
					result = self.analyze(article)
				request.delete()
				Request.flush()
			time.sleep(1)

	def send_to_api(self, text, language, resource):
		try:
			document = client.specific_resource_analysis(
				body={"document": {"text": text}}, 
				params={'language': language, 'resource': resource})

		except ExpertAiRequestError as e:
			if e.text.startswith("Failed to fetch the Bearer Token"):
				print("Invalid ExpertAi password. Please reconfigure Config/Config.xml")
				exit(0)
			else:
				raise
		return document
			

	def enrich(self, text):
		sentiment_output   = self.send_to_api(text, 'en', 'sentiment')
		complexity_output  = self.send_to_api(text, 'en', 'deep-linguistic-analysis')
		try:
			
			record = {"sentiment_expertai_postive":	 sentiment_output.sentiment.postive,
				  "sentiment_expertai_negative": sentiment_output.sentiment.negative,
				  "complexity_expertai": 0.0}
		except AttributeError as e:
			traceback.print_tb()
			

		return record
			
		
	def complexity(self, text):
		tokens = tokenize.word_tokenize(text)
		tokens = [token.lower() for token in tokens if not(token in (".", ","))]
		tokens = [token for token in tokens if not token in corpus.stopwords.words("english")]
		clean_length  = max(1, len(" ".join(tokens)))
		word_length   = clean_length/max(1, len(tokens))
		punctuation   = len(text)/clean_length
		ps	      = stem.PorterStemmer()
		stemmed	      = set([ps.stem(token) for token in tokens])
		complexity    = len(" ".join(stemmed))/clean_length
		duplication   = len(tokens)/max(1, len(stemmed))
		return {"complexity_word_length":	word_length,
			"complexity_clean_length":	clean_length,
			"complexity_punctuation":	punctuation,
			"complexity_complexity":	complexity,
			"complexity_duplication":	duplication,
			"complexity_score":		-1*(word_length + complexity - duplication)
			}
			
	def analyze(self, article):
		text_object		     = NRCLex(article.content)
		sentiment		     = text_object.affect_frequencies
		complexity		     = self.complexity(article.content)
		
		record			     = {}
		record["id"]		     = article.id
		record["publisher"]	     = article.publisher
		record["platform"]	     = article.platform
		for (key, value) in sentiment.items():
			record["sentiment_{0:s}".format(key)] = value
		for (key, value) in complexity.items():
			record[key] = value
		record["sentiment"]	     = sentiment["positive"] - sentiment["negative"]
		record["sentiment_score"]    = sentiment["anger"]  - sentiment["sadness"]
		record["sentiment_score2"]   = sentiment["anger"] + sentiment["fear"]  - 2*sentiment["sadness"] - sentiment["trust"]
		record["capital_score"]	     = sum(1 for letter in article.content if letter.isupper())/max(1, len(article.content))
		record["article_length"]     = len(article.content)
		trust			     = TrustArticle.fromJSON(record)
		self.score(record)
		return True

	def score(self, record):
		Log.info("Scoring")
		if not(self.m_parameters):
			return
		a1 = self.m_parameters.article_length["ci10"]
		b1 = self.m_parameters.article_length["scale"]
		a2 = self.m_parameters.sentiment_score["ci90"]
		b2 = self.m_parameters.sentiment_score["scale"]
		y1 = max(0, 1-b1*(record["article_length"]-a1))
		c2 = math.exp(-a2 - b2*record["sentiment_score2"])
		y2 = 1/(1+c2)
		
		trust = {"id":			record["id"],
			 "param_version":	self.m_parameters.version,
			 "trust_score":		max(0, min(100, 100-100*y1*y2)),
			 "sentiment_score":	max(0, min(100, 100-100*y2)),
			 "divergency_score":	100,
			 "layout_score":	max(0, min(100, 100-100*y1)),
			 "complexity_score":	100.0,
			 "platform_score":	100.0,
			 "author_score":	100.0,
			 "reasons":		"[]"
		}
		trust = Trust.fromJSON(trust)
		trust.flush()
		
	
	def clean(self):
		""" Frees up space from old algorithms
		"""
		Trust.clean()

	def calibrate(self):
		Article.requeue()
		
		version		= TrustParameters.getVersion()+1
		factors		= ["sentiment_score", "article_length", "complexity_punctuation", "complexity_wordlength", "complexity_complexity", "complexity_duplication"]

		record = {"version": version,
			  "platform":  "",
			  "publisher": ""}
		for factor in factors:
			ci = TrustAritcle.ci(factor)
			ci["scale"] = (ci["ci90"] - ci["ci10"])
			record[factor] = ci
		parameters = TrustParameters.fromJSON(record)
		parameters.flush()
		for (i, item) in enumerate(Article.all()):
			self.score(item)
			if (i % 1000 == 0):
				print(i)
		
	def recalculate(self):
		TrustArticle.clean()
		Article.requeue()


	def parse_document(self, id, data):
		Log.info("ParseDocument", id, data, type(data))
		record = {}
		record["id"]	     = id
		try:
			if (isinstance(data, str)):
				data = json.loads(data)				       
			record["content"]    = data["content"]
			record["title"]	     = data["title"]
			record["author"]     = data["author"]
			record["publisher"]  = data["publisher"]
			record["platform"]   = "IPFS"
			
			      
		except (KeyError, ) as e:
			record["content"]    = str(data)
			record["title"]	     = ""
			record["author"]     = ""
			record["publisher"]  = ""
			record["platform"]   = "IPFS"
		Log.info("ParseDocument", id, record)
		article = Article.fromJSON(record)
		article.flush()
		self.analyse(article)
		Log.info("ParseDocument - Analysis Done", id, record)
		request = Request.get(id)
		request.delete()
		
		
	def download(self, request):
		ipfs_hash = re.sub("IPFS_", "", request.id)
		self.m_ipfs_gateway.retrieveDocumentFromHash(ipfs_hash, lambda x: self.parse_document(request.id, x))
	
	def start(self):
		if (self.m_run):
			return
		self.m_run = True
		super(Analyzer, self).start()

	def stop(self):
		self.m_run = False


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
				


