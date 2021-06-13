import requests
import pymongo
import json
import time
import sys

client	 = pymongo.MongoClient("mongodb://localhost:27017/")
db	 = client["bywire"]
articles = db["articles"]
analyzer = "http://127.0.0.1:5055"
routes	 = {'recalculate':  analyzer+'/parameters/recalculate',
	    'calibrate':    analyzer+'/parameters/calibrate'
	    'clean':	    analyzer+'/parameters/clean'
}

print(sys.argv)
if (len(sys.argv) < 2):
	print("Enter a command")
	exit(0)

request = requests.post(routes[sys.argv[1], params={})
print(request)
print(request.text)



