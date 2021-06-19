import requests
import pymongo
import json
import time

client	 = pymongo.MongoClient("mongodb://localhost:27017/")
db	 = client["bywire"]
articles = db["articles"]
analyzer = "http://127.0.0.1:5055"
routes	 = {'text':  analyzer+'/analyze/text',
	    'query': analyzer+'/analyze/query'}

for (i, item) in enumerate(articles.find()):
	if i < 256000:
		continue
	#print(i)
	if i%1000 == 0:
		print(i)
		time.sleep(10)
	record = {'content':   item['content'],
		  'title':     item['title'],
		  'platform':  "bywire",
		  'author':    item['author'] if 'author' in item else "",
		  'publisher': item['publisher'] if 'publisher' in item else ""}
	for (key, value) in record.items():
		record[key] = record[key] if record[key] else ""
	request = requests.post(routes['text'], params=record)
	response = json.loads(request.text)
	id = response["id"]
	if response["new"]:
		time.sleep(0.01)




