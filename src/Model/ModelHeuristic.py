import os, os.path
import re
import json
from datetime import datetime, timedelta

from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from Model.ModelConst import ModelConst

from Model.Model import Model

class ModelHeuristic(Model):
	""" Model: Virtual Base class for models
	"""
	def __init__(self, config):
		super(ModelHeuristic, self).__init__(config)

	def predict(self, features):
		norm	   = lambda x: 100*max(0, min(1, 1-x))
		sentiment  = norm(features["sentiment2"])
		layout	   = norm(1/2*(features["article_length"] + features["punctuation"]))
		divergency = norm(features["divergency"])
		complexity = norm(1/3*(features["complexity_complexity"] + features["complexity_duplication"] + features["complexity_word_length"]))
		platform   = norm(features["platform"])
		author	   = norm(features["author"])
		trust	   = (2*sentiment + complexity + layout + platform + divergency)/6
		
		record = {  "trust_score":	trust,
			    "divergency_score": divergency,
			    "sentiment_score":	sentiment,
			    "layout_score":	layout,
			    "complexity_score": complexity,
			    "author_score":	author,
			    "platform_score":	platform
		}
		return record;
				
	def train(self):
		pass
		
	def save(self):
		pass
				
	def load(self):
		pass


