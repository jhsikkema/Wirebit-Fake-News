import os, os.path
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from flask import Response, request
import re
import codecs
import json
from Server.Analyzer import Analyzer
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from datetime import datetime, timedelta
from Util.DataUtil import DataUtil
from Server.Parsers import analyze_text_parser, analyze_ipfs_parser, analyze_query_parser
from Server.Messages import Messages
from Database.Trust import Trust
from Database.Article import Article
from Database.Request import Request
global ipfs_server


class AnalyzeText(Resource):
	def post(self):
		data	= analyze_text_parser.parse_args()
		data	= DataUtil.clean_data(data)
		article = Article.fromJSON(data)
		found	= Article.get(article.id)
		if (found):
			del article
			return {"id": found.id, "new": True}, 200
		request = Request.fromJSON(article.toJSON())
		article.flush()
		request.flush()
		return {"id": request.id, "new": True}, 200

class AnalyzeIPFS(Resource):
	def post(self):
		data	= analyze_ipfs_parser.parse_args()
		data	= DataUtil.clean_data(data)
		Log.info(data)
		record	= {}
		id	     = Article.genID("", data["ipfs_hash"])
		if (Article.get(id)):
			return {"id": id, "new": True}, 200
		record["id"] = id
		request = Request.fromJSON(record)
		request.flush()
		return {"id": id, "new": True}, 200

class AnalyzeQuery(Resource):
	def post(self):
		data	= analyze_query_parser.parse_args()
		data	= DataUtil.clean_data(data)
		Log.info("AnalyzeQuery", data)
		id	= re.sub("\\\\", "", data["id"])
		Log.info("AnalyzeQuery", id)
		if (Request.get(id)):
			Log.info("AnalyzeQuery - Got Query")
			return {"id": id, "status": "Processing", "done": False}, 200
		trust	= Trust.get(id)
		if not(trust):
			Log.info("AnalyzeQuery - Got Trust")
			return {"id": id, "status": "Unknown Request", "done": True}, 200
		msg = {"id": id, "status": "Done", "done": True, "data": trust.toJSON()}
		if (request.fromIPFS):
			article = Article.get(id)
			msg["text"] = article.content
		Log.info("AnalyzeQuery - DONE", msg)
		return msg, 200

class AnalyzeFlag(Resource):
	def post(self):
		data	= analyze_flag_parser.parse_args()
		data	= DataUtil.clean_data(data)
		id	= data["id"]
		trust	= TrustFlagged.get(id)
		if not(trust):
			trust = TrustFlagged.fromJSON({"id":	      id,
						       "is_fake":     True,
						       "expert_vote": 0,
						       "reader_vote": 0})
		if (data["is_expert"]):
			trust.expert_vote += 1
		else:
			trust.reader_vote += 1
		trust.flush()
		return {"status": "Done", "done": True}, 200

class RecalculateParameters(Resource):
	def post(self):
		analyzer = Analyzer.get()
		analyzer.recalculate()
		return {}, 200

class CalibrateParameters(Resource):
	def post(self):
		analyzer = Analyzer.get()
		analyzer.calibrate()
		return {}, 200


class CleanParameters(Resource):
	def post(self):
		analyzer = Analyzer.get()
		analyzer.clean()
		return {}, 200



class BrewCoffee(Resource):
	def post(self):
		return Response("I'm a teapot", status=418, mimetype='application/coffee-pot-command')

			
