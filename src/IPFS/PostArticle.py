import os, os.path
import json
import time
import requests
from requests.auth import HTTPBasicAuth
import re

if __name__=="__main__":
	import sys
	print(os.getcwd())
	sys.path.append(os.path.join(os.getcwd(), ".."))

	
from datetime import datetime, timedelta

from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from Database.User import User


class PostArticle(object):
	def __init__(self, config):
		Log.info("PostArticle - init")

		self.m_config		    = config
		self.m_url		    = config[Const.WEB_URL]
		self.m_publish_endpoint	    = config[Const.WEB_PUBLISH_ENDPOINT]
		self.m_api_key		    = config[Const.WEB_API_KEY]
		self.m_default_publisher_id = config[Const.WEB_DEFAULT_PUBLISHER_ID]
		Log.info("PostArticle - ", self.m_url, self.m_publish_endpoint, self.m_api_key)

	def send(self, article):
		Log.info("PostArticle - send")
		user		     = User.get(article.publisher)
		publisher_website_id = user.website_id if user else ""
		publisher_website_id = publisher_website_id if publisher_website_id else self.m_default_publisher_id
		url		     = self.m_url+"/"+self.m_publish_endpoint+"?apiKey="+self.m_api_key

		#summary = re.sub("<.*?>", "", article.content, flags=re.DOTALL)
		#summary = summary[0:410]
		#match	= re.match("^(.*)[.]? [^ ]*?$", summary, flags=re.DOTALL)
		#summary = match.group(1) if match else summary
		#summary = summary + "..."
		summary	 = ""
		Log.info("PostArticle - url", url)

		headers = {"Accept-Encoding": "gzip, deflate, br",
			   'Content-Type': 'application/json'}

		auth	      = HTTPBasicAuth("apiKey", self.m_api_key)
		content	      = article.content
		image	      = article.image if article.share_images else ""
		image	      = re.sub("\\\\", "", image)
		if (image == ""):
			image	       = re.search('<img.*?src="(.+?)"', article.content)
			image	       = image.group(1) if image else ""
			content	       = re.sub('<img.*?>', "", article.content, count=1)
		image_caption = article.image_caption if article.share_images else ""
		gallery	      = [] if article.share_images else []
		#article.content = re.sub('<img.*?>', "", article.content, count=1)
		is_wrapped    = re.match("^\s*<p>(.*?)</p>\s*$", content, flags=re.DOTALL)
		content = "<p>"+re.sub("\n+", "</p>\n<p>", content)+"</p>" if not is_wrapped else content
		#content = re.sub('<p>', '', re.sub('</p>', '', content))
		body = {
			"publisherId": publisher_website_id,
			"authorId":    publisher_website_id,
			"model": {
				"title": article.title,
				"html":	 content,
				"link": "",
				"canonical": "",
				"summary":	summary,
				"image":	image,
				"imageCaption": image_caption,
				"gallery":	gallery,
				"botsNoIndex": False,
				"video": "",
				"audio": "",
				"status": "published",
				"categoryIds": [],
				"timestamp": article.timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
			}
			}
		Log.info("PostArticle - ", article.revision, body)
		#try:
		if article.revision > 1:
			Log.info("PUT")
			req = requests.put(url, allow_redirects=False, headers=headers , auth=auth , data=json.dumps(body))

		else:
			Log.info("POST")
			req = requests.post(url, allow_redirects=False, headers=headers, auth=auth, data=json.dumps(body))
		#except:
		#	Log.exception()
		Log.info("PostArticle", req.text)
		Log.info("PostArticle", req)


if __name__ == "__main__":
	class Post (object):
		def __init__(self, title, content):
			self.content = title
			self.title   = content
			self.revision = 0
			self.timestamp = datetime.now()
	config_path = os.path.join(os.getcwd(), "..", Const.CONFIG_PATH)
	print(config_path)
	with Config(config_path) as config:
		log = Log(config)
		i = 2
		post = Post("Test Post {0:d}".format(i), "This is test post {0:d}".format(i))
		poster = PostArticle(config)
		poster.send(post)
