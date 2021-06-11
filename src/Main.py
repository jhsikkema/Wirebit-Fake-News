import os, os.path
import sys
from gevent import monkey
monkey.patch_all(subprocess=True)
from datetime import datetime
import time
import json
import threading
import re
import codecs
import signal

from IPFS.IPFSServer import IPFSServer
from IPFS.IPFSConst import IPFSConst
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

global ipfs_server, config, PARAMETER_VERSION


app = Flask(__name__)
#app.config['PROFILE'] = True
#app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

api = Api(app)

from Server import Resources

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

@app.route('/')
def index():
    pass


config = Config(Const.CONFIG_PATH)
config.__enter__()
log = Log(config)
Log.info(config[IPFSConst.CONFIG_READ_ONLY_SERVER], IPFSConst.CONFIG_READ_ONLY_SERVER)
ipfs_server = IPFSServer(config, config[IPFSConst.CONFIG_READ_ONLY_SERVER].lower() == 'false')
ipfs_server.start()
analyzer = Analyzer.get(config)
analyzer.start()
#api.add_resource(Resources.UserRegistration,		'/registration')
#api.add_resource(Resources.UserLogin,			'/login')
#api.add_resource(Resources.UserLogoutAccess,		'/logout')
#api.add_resource(Resources.UserLogoutRefresh,		'/logout/refresh')
#api.add_resource(Resources.TokenRefresh,		'/token/refresh')
#api.add_resource(Resources.GenerateKeys,		'/generatekeys')

api.add_resource(Resources.CalculateParameters,		'/parameters/calculate')
api.add_resource(Resources.AnalyzeText,			'/analyze/text')
api.add_resource(Resources.AnalyzeIPFS,			'/analyze/ipfs')
api.add_resource(Resources.AnalyzeQuery,		'/analyze/query')

@app.teardown_appcontext
def shutdown_session(exception=None):
	if exception:
		global wallets, config, beat, ipfs_server, trust_explorer
		db_session.remove()
		analyzer.stop()
		ipfs_server.stop()
		config.__exit__(None, None, None)
		

if __name__=='__main__':
	print("Running Main")
	cProfile.run("app.run(host='127.0.0.1', port='5030')", "profile.prof")
