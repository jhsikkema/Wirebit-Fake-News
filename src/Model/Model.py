import os, os.path
import json
from datetime import datetime, timedelta
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log

from Database.Trust	      import Trust
from Database.TrustArticle    import TrustArticle
from Database.TrustParameters import TrustParameters
from Model.ModelConst import ModelConst

class Model(object):
	VERSION = "0.1"
	""" Model: Virtual Base class for models
	"""
	def __init__(self, config):
		super(Model, self).__init__()
		self.m_config		      = config
		self.m_parameters	      = dict([(item.platform, item) for item in TrustParameters.get(TrustParameters.getVersion())])
		self.m_param_version	      = min([item.version for item in self.m_parameters.values()])
		Model.VERSION		      = config[ModelConst.VERSION]
		print(Model.VERSION)
		print(type(Model.VERSION))
		base_path	  = config[ModelConst.BASE_PATH]
		print(base_path)
		self.m_model_path = os.path.join(base_path, "model_{0:s}.json".format(Model.VERSION))
		self.m_coeff_path = os.path.join(base_path, "coeff_{0:s}.h5".format(Model.VERSION))

	def flagged(self, trust_article):
		flag = TrustFlagged.get(trust_article.id)
		if not(flag):
			return 0
		return 2*flag.reader.strength/200 + 1

		
	def features(self, trust_article):
		parameters	       = self.m_parameters[platform]
		platform	       = trust_article.platform if trust_article.platform in self.m_parameters else ModelConst.PLATFORM_ALL
		
		a1  = parameters.sentiment_score2["ci90"]
		b1  = parameters.sentiment_score2["scale"]
		a2  = parameters.sentiment_score2["ci90"]
		b2  = parameters.sentiment_score2["scale"]
		a3  = parameters.article_length["ci10"]
		b3  = parameters.article_length["scale"]
		a41 = parameters.complexity_punctuation["ci10"]
		a42 = parameters.complexity_punctuation["ci90"]
		a5  = parameters.complexity_word_length["ci10"]
		a6  = parameters.complexity_complexity["ci10"]
		a7  = parameters.complexity_duplication["ci10"]
		a8  = min(parameters.sentiment_expertai_positive["ci90"], parameters.sentiment_expertai_negative["ci90"])
		s91pos = parameters.sentiment_expertai_positive["ci90"]
		s91neg = parameters.sentiment_expertai_negative["ci90"]
		s91com = parameters.complexity_expertai["ci50"]
		s92pos = parameters.sentiment_positive["ci90"]
		s92neg = parameters.sentiment_negative["ci90"]
		s92    = parameters.complexity_complexity["ci50"]
		# Positive Divergence
		if (trust_article.sentiment_expertai_positive >= 0):
			div_pos = math.abs(trust_article.sentiment_expertai_positive/s91pos - trust_article.sentiment_positive/s92pos)
		else:
			div_pos = 0
		# Negative Divergence
		if (trust_article.sentiment_expertai_negative >= 0):
			div_neg = math.abs(trust_article.sentiment_expertai_negative/s91neg - trust_article.sentiment_positive/s92neg)
		else:
			div_neg = 0
		# Complexity Divergence
		if (trust_article.complexity_expertai >= 0):
			div_com = math.abs(trust_article.complexity_expertai/s91com - trust_article.complexity_complexity/s92com)
					   
			
		norm = lambda x: max(0, min(1, x))
		record = {"sentiment":		    norm((trust_article.sentiment_score - a1)/b1),
			  "sentiment2":		    norm((trust_article.sentiment_score2 - a2)/b2),
			  "article_length":	    norm((a3 - trust_article.article_length)/b3),
			  "punctuation": 1 if (trust_article.complexity_punctuation < a41 or
					       trust_article.complexity_punctuation > a42) else 0,
			  "complexity_complexity":  1 if (trust_article.complexity_complexity  < a6) else 0,
			  "complexity_duplication": 1 if (trust_article.complexity_duplication < a7) else 0,
			  "complexity_word_length": 1 if (trust_article.complexity_word_length < a5) else 0,
			   "platform":	  platforms[trust_articles.platform] if (trust_article.platform) in platforms else 0.5,
			  "divergency":	  norm(max(div_pos, div_neg, div_com)),
			  "author":	 1
			  }
		return record		     

	
	def score(self, trust_article):
		if not(self.m_parameters):
			return
		platform	       = trust_article.platform if trust_article.platform in self.m_parameters else ModelConst.PLATFORM_ALL
		parameters	       = self.m_parameters[platform]
		features	       = self.features(trust_article)
		trust		       = self.predict(features)
		trust["id"]	       = trust_article.id
		trust["param_version"] = self.m_param_version
		trust = Trust.fromJSON(trust)
		trust.flush()
		return trust
		
	def predict(self, features):
		assert False, "Model.predict - Model is a virtual base class"
				
	def train(self):
		assert False, "Model.predict - Model is a virtual base class"
		
	def save(self):
		assert False, "Model.predict - Model is a virtual base class"
				
	def load(self):
		assert False, "Model.predict - Model is a virtual base class"
				
