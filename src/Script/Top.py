import requests
import pymongo
import json
import time
import os, os.path
import re
import codecs
from matplotlib import pyplot

path	     = os.path.join("..", "Data", "Analysis")
client	     = pymongo.MongoClient("mongodb://localhost:27017/")
db	     = client["bywire_trust"]
trust	     = db["trust_articles"]
articles     = db["articles"]
limit	     = 25
filter_blank = True
measures = [#"sentiment",
	    "sentiment_anger",
	    "sentiment_fear",
	    "sentiment_anticip",
	    "sentiment_trust",
	    "sentiment_surprise",
	    "sentiment_sadness",
	    "sentiment_disgust",
	    "sentiment_joy",
	    "sentiment_positive",
	    "sentiment_negative",
	    "sentiment_score",
	    "complexity_word_length",
	    "complexity_clean_length",
	    "complexity_punctuation",
	    "complexity_complexity",
	    "complexity_duplication",
	    "complexity_score",
	    "capital_score",
	    "article_length"]

for measure in measures:
	print(measure)
	with codecs.open(os.path.join(path, measure+"_bottom.csv"), 'w', encoding='UTF-8') as outfile:
		for item in trust.find().sort([[measure, pymongo.ASCENDING]]).limit(limit):
			score	= "{0:.3f}".format(item[measure])
			id	= item["id"]
			article = articles.find({"id": item["id"]}).limit(1)[0]
			if filter_blank and not(article["content"].strip()):
				continue
			title	= article["title"]
			content = re.sub("\n", "", article["content"], flags=re.DOTALL)
			outfile.write(";".join([score, id, title, content]))
			outfile.write("\n\n\n")
	with codecs.open(os.path.join(path, measure+"_top.csv"), 'w', encoding='UTF-8') as outfile:
		for item in trust.find().sort([[measure, pymongo.DESCENDING]]).limit(limit):
			score	= "{0:.3f}".format(item[measure])
			id	= item["id"]
			article = articles.find({"id": item["id"]}).limit(1)[0]
			if filter_blank and not(article["content"].strip()):
				continue
			title	= article["title"]
			content = re.sub("\n", "", article["content"], flags=re.DOTALL)
			outfile.write(";".join([score, id, title, content]))
			outfile.write("\n\n\n")
			

	data = [item[measure] for item in trust.find()]
	pyplot.figure()
	pyplot.hist(data, bins=100)
	pyplot.savefig(os.path.join(path, measure+"_histo.png"))
