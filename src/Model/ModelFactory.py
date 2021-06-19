import os, os.path
import json
from datetime import datetime, timedelta
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log

from Model.ModelANN import ModelANN
from Model.ModelHeuristic import ModelHeuristic
from Model.ModelConst import ModelConst

class ModelFactory(object):
	""" ModelFactory: FactoryClass to generate Models
	"""
	@classmethod
	def build(cls, config):
		if config[ModelConst.TYPE].lower() == ModelConst.TYPE_HEURISTIC:
			return ModelHeuristic(config)
		if config[ModelConst.TYPE].lower() == ModelConst.TYPE_ANN:
			return ModelANN(config)
