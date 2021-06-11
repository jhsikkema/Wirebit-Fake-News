import os, os.path
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Response, request
from Server.Models import User, RevokedToken
import re
import codecs
import json
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from datetime import datetime, timedelta
from Util.DataUtil import DataUtil
from Server.Parsers import analyze_text_parser, analyze_ipfs_parser, analyze_query_parser
from Server.Messages import Messages
from Database.Article import Article
global ipfs_server


class AnalyzeText(Resource):
	def post(self):
		data	= analyze_text_parser.parse_args()
		data	= DataUtil.clean_data(data)
                article = Article.fromJSON(data)
                request = Request.fromJSON(article.toJSON())
                article.flush()
                request.flush()
                return {"id": request.id}, 200

class AnalyzeIPFS(Resource):
	def post(self):
		data	= analyze_ipfs_parser.parse_args()
		data	= DataUtil.clean_data(data)
                record["id"] = Article.genID("", data["ipfs_hash"])
                request = Request.fromJSON(record)
                request.flush()
                return {"id": request.id}, 200

class AnalyzeQuery(Resource):
	def post(self):
		data	= analyze_query_parser.parse_args()
		data	= DataUtil.clean_data(data)
                id      = data["request_id"]
                if (request.get(id)):
                        return {"status": "Processing", "done": False}
                
                record["id"] = Article.genID("", data["ipfs_hash"])
                request = Request.fromJSON(record)
                request.flush()
                return {"id": request.id}, 200

class CalculateParameters(Resource):
	def post(self):
                
                record["id"] = Article.genID("", data["ipfs_hash"])
                request = Request.fromJSON(record)
                request.flush()
                return {"id": request.id}, 200



class BrewCoffee(Resource):
	def post(self):
		return Response("I'm a teapot", status=418, mimetype='application/coffee-pot-command')

			
