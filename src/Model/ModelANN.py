import os, os.path
import re
import json
from datetime import datetime, timedelta

from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from Model.ModelConst import ModelConst

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
 
from Model.Model import Model
from Database.Article	      import Article
from Database.TrustArticle    import TrustArticle


class ModelANN(Model):
	""" Model: Virtual Base class for models
	"""
	def __init__(self, config):
		super(ModelANN, self).__init__(config)
		self.m_model = None
		self.m_columns = ["sentiment2", "article_length", "punctuation", "divergency", "complexity_complexity", "complexity_duplication", "complexity_word_length", "platform"]
		self.create()
		
	def create(self):
		self.m_model = Sequential()
		layers	     = self.m_config[ModelConst.ANN_LAYERS]
		self.m_model.add(Dense(int(layers[0]), input_dim=8, activation='relu'))
		for layer in layers[1:]:
			self.m_model.add(Dense(int(layer), activation='relu'))
		self.m_model.add(Dense(1, activation='sigmoid'))
		self.m_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
		

	def predict(self, features):
		X = np.array([[features[key] for key in self.m_columns]])
		score = self.m_model.predict_classes(X)
		record = {  "trust_score":	100*(1-score),
			    "divergency_score": divergency,
			    "sentiment_score":	sentiment,
			    "layout_score":	layout,
			    "complexity_score": complexity,
			    "platform_score":	platform
		}
		
		return record
	
	def train(self):
		X = []
		Y = []
		for item in Article.all():
				trust	 = TrustArticle.get(item.id)
				flag	 = self.flagged(item.id)
				features = self.features(trust)
				X.append([features[key] for key in self.m_columns])
				Y.append(flag)
		X = np.array(X)
		Y = np.array(Y)

		epochs	   = int(self.m_config[ModelConst.ANN_EPOCHS])
		batch_size = int(self.m_config[ModelConst.ANN_BATCHSIZE])
		self.m_model.fit(X, Y, epochs=epochs, batch_size=batch_size, verbose=0)
		scores = self.m_model.evaluate(X, Y, verbose=0)
		print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
		
	def save(self):
		model_json = self.m_model.to_json()
		with open(self.m_model_path, "w") as outfile:
			outfile.write(model_json)
		# serialize weights to HDF5
		self.m_model.save_weights(self.m_coeff_path)
				
	def load(self):
		# load json and create model
		with open(self.m_model_path, 'r') as infile:
			model_json = infile.read()
			self.m_model = model_from_json(model_json)
		self.m_model.load_weights(self.m_coeff_path)
		self.m_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
		
