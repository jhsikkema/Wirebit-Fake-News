import requests
import pymongo

client	 = pymongo.MongoClient("mongodb://localhost:27017/")
db	 = client["bywire"]
articles = db["articles"]
analyzer = "localhost:5055"
routes	 = {'text':  analyzer+'/analyze/text',
	    'query': analyzer+'/analyze/query',

for item in articles.find():
	print(item)
	print(routes['text']
	exit(1)
	request = requests.post(routes['text'], json=item)
	print(request)
	print(request.status_code)
	for i in range(100000):
		request = requests.post(routes['query'], json=item)
		print(request)
		time.sleep(1)





