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
		print(features)
		Log.info(features)
		norm	   = lambda x: 100*max(0, min(1, 1-x))
		sentiment  = norm(0.75*features["sentiment2"]+0.75*features["euphoria"])
		layout	   = norm(0.75*features["article_length"] + 0.75*features["punctuation"])
		divergency = norm(features["divergency"])
		complexity = norm(0.5*features["complexity_complexity"] + 0.5*features["complexity_duplication"] + 0.5*features["complexity_word_length"])
		platform   = norm(features["platform"])
		author	   = norm(features["author"])
		trust	   = (3*sentiment + complexity + layout + platform + divergency)/7
		trust	   = max(1, 100+0.75*(sentiment-100) + 0.33*(complexity-100) + 0.33*(layout - 100) + 0.33*(platform-100) + 0.33*(divergency-100))
		
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


