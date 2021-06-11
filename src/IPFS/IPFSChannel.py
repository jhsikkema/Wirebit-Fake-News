import os, os.path
import re
import time
import glob
import dateutil.parser
import codecs
import json
from collections import deque
import hashlib
import threading
from datetime import datetime, timedelta
import sys
import io
import queue
from collections import deque
import subprocess
from Util.Const import Const
from Util.Config import Config
from Util.Log import Log
from Util.CSVFile import CSVFile
from IPFS.ipfs import IPFSGateway
from IPFS.IPFSConst import IPFSConst
from Database.Article import Article
from IPFS.ArticleIndex import ArticleIndex


class IPFSChannel(object):
	ACTION = ""
	def __init__(self, config, ipfs_gateway):
		self.m_config	       = config
		server_mode	       = self.m_config[IPFSConst.SERVER_MODE].lower()
		assert server_mode in [IPFSConst.SERVER_MODE_SINGLE,
				       IPFSConst.SERVER_MODE_SLAVE,
				       IPFSConst.SERVER_MODE_MASTER], "IPFSServer - Invalid Server Mode: {0:s}".format(server_mode)
		self.m_server_is_standalone	= (server_mode == IPFSConst.SERVER_MODE_SINGLE)
		self.m_server_is_master	      = (server_mode == IPFSConst.SERVER_MODE_MASTER)
		self.m_server_is_slave	      = (server_mode == IPFSConst.SERVER_MODE_SLAVE)
		self.m_ipfs_gateway    = ipfs_gateway
		self.m_ipfs_path       = self.m_config[IPFSConst.IPFS_PATH]
		self.m_ipfs_channel_path = os.path.join(self.m_ipfs_path, self.m_config[IPFSConst.IPFS_OUTPUT])
		self.m_ipfs_channel_queue = None
		self.m_ipfs_channel_process = None
		self.m_current_channel = ""
		self.checkChannelID()
		self.m_node	       = self.m_config[IPFSConst.IPFS_NODE]
		self.m_sequence_nr     = 0
		self.m_lock	       = threading.Condition()
		self.m_message_queue   = deque()
	
	def channelID(self):
		utctime	     = datetime.now()
		channel_name = IPFSConst.CHANNEL_NAME.format(self.ACTION, utctime.strftime('%Y%m%d'))
		return hashlib.md5(channel_name.encode()).hexdigest()

	def checkChannelID(self):
		channel = self.channelID()
		if (channel != self.m_current_channel):
			self.disconnect()
			self.m_current_channel = channel
			self.connect()

	def connect(self):
		if (self.m_server_is_standalone):
			return
		cmd = [os.path.join(self.m_ipfs_path, 'ipfs'), 'pubsub', 'sub', self.m_current_channel]
		Log.info('IPFSChannel - connect', cmd)
		ON_POSIX = 'posix' in sys.builtin_module_names
		self.m_ipfs_channel_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=ON_POSIX)

		def enqueue_output(out, queue):
			for line in iter(out.readline, b''):
				queue.put(line)
			out.close()

		self.m_ipfs_channel_queue = queue.Queue()
		t = threading.Thread(target=enqueue_output, args=(self.m_ipfs_channel_process.stdout, self.m_ipfs_channel_queue))
		t.daemon = True
		t.start()


	def disconnect(self):
		if (self.m_server_is_standalone):
			return
		if (self.m_ipfs_channel_process):
			self.m_ipfs_channel_process.kill()

	def __del__(self):
		self.disconnect()


	def hasMessages(self):
		return len(self.m_message_queue)>0
	
	def receiveMessageCallback(self, msg):
		pass

	def checkMessages(self):
		if (self.m_server_is_standalone):
			return []
		try:
			data = self.m_ipfs_channel_queue.get_nowait() # or q.get(timeout=.1)
		except queue.Empty:
			return
		Log.info('IPFSChannel - checkMessages', data)
		data = data.decode('utf-8')
		data = data.split('\n')
		Log.info('IPFSChannel - checkMessages', data)
		messages = [item for item in data if len(item)]
		messages = [item for (index, item) in enumerate(messages) if index >= self.m_sequence_nr]
		for msg in messages:
			msg = json.loads(msg)
			with self.m_lock:
				self.m_message_queue.append(msg)
		print(messages)

	
	def receive(self):
		if self.m_server_is_standalone:
			return
		msg = None
		with self.m_lock:
			msg = self.m_message_queue.pop()
		Log.info('recieve', msg)
		if not(msg['action'] == self.ACTION):
			return
		if msg['node'] == self.m_node:
			return
		self.receiveMessageCallback(msg)

	def sendMessage(self, msg):
		msg['action'] = self.ACTION
		msg['sender'] = self.m_node
		self.m_ipfs_gateway.publish(self.m_current_channel, json.dumps(msg))

	def logCallback(self, data):
		Log.info('Callback', data)

class IPFSMasterSlaveChannel(IPFSChannel):
	def send(self, msg):
		if (self.m_server_is_slave):
			return
		super(IPFSMasterSlaveChannel, self).sendMessage(msg)
	

class HashChannel(IPFSMasterSlaveChannel):
	ACTION = 'HASH'
	def send(self, hash):
		msg = {'data': hash}
		super(HashChannel, self).send(msg)
		
	def recieveMessageCallback(self, msg):
		self.m_ipfs_gateway.setPin(msg['data'], self.logCallback)


class IndexChannel(IPFSMasterSlaveChannel):
	ACTION = 'INDEX'
	def send(self):
		msg = {'data': hash}
		super(IndexChannel, self).send(msg)


	def parseIndex(self, data):
		Log.info(data)
	
		
	def recieveMessageCallback(self, msg):
		self.m_ipfs_gateway.retrieveDocumentFromHash(msg['data'], self.parseIndex)


class PeerChannel(IPFSChannel):
	ACTION = 'PEER'
	def __init__(self, config, ipfs_gateway):
		super(PeerChannel, self).__init__(config, ipfs_gateway)
		self.m_peers_file      = os.path.join(self.m_config[Const.STORAGE_BASE_PATH], self.m_config[IPFSConst.IPFS_PEERS_FILE])
		self.m_ipfs_port = self.m_config[IPFSConst.CONFIG_SERVER_PORT]
		if (self.m_config[IPFSConst.IPFS_PEER_IP_STABLE].lower() == 'true'):
			self.m_peer_id = self.m_config[IPFSConst.IPFS_PEER_IP_ADDRESS]
		else:
			os.system("{0:s} > ip.log".format(self.m_config[IPFSConst.IPFS_PEER_IP_COMMAND]))
			with open('ip.log', 'r') as infile:
				self.m_peer_id = "".join([item for item in infile])
		self.m_peer_ref	       = self.m_config[IPFSConst.IPFS_PEER_REF]
		self.m_sequence_nr     = 0	 
			
		self.m_peers	       = {}
		self.read_peers()
		Log.info('Peers', self.m_peers)

	def write_peers(self):
		if (self.m_server_is_standalone):
			return

		with CSVFile(self.m_peers_file, 'w', ';') as outfile:
			Log.info('write-peers', self.m_peers)
			for peer in self.m_peers.values():
				Log.info('write-peers', [key for key in peer.keys()])
				outfile.header = [key for key in peer.keys() if key]
				Log.info('write-peers', outfile.header)
				if isinstance(peer['last-update'], datetime):
					peer['last-update'] = peer['last-update'].strftime('%Y%m%d %H:%M:%S')
				Log.info('write-peers', peer)
				outfile.write(peer)
			Log.info(self.peer_id())
			outfile.write(self.peer_id())

	def read_peers(self):
		if (self.m_server_is_standalone):
			return
		with CSVFile(self.m_peers_file, 'r', ';') as infile:
			Log.info([(peer['id'], peer) for peer in infile])
		with CSVFile(self.m_peers_file, 'r', ';') as infile:
			self.m_peers = dict([(peer['id'], peer) for peer in infile if not(peer['id'] == self.m_peer_id)])
			for peer in self.m_peers.values():
				peer['last-update'] = datetime.strptime(peer['last-update'], '%Y%m%d %H:%M:%S')
		Log.info('read-peers', self.m_peers)
		Log.info('read-peers', self.m_peer_id)

	def peer_id(self):
		protocol = "ip4" if (re.match("([0-9]{1, 3}[.]){3}[0-9]{1,3}", self.m_peer_id)) else "ip6"
		address = "/{0:s}/{1:s}/tcp/{2:s}/{3:s}".format(protocol, self.m_peer_id, self.m_ipfs_port, self.m_node)
		data = {'id': self.m_peer_id,
			'link': address,
			'ping-hash': self.m_peer_ref,
			'last-update': datetime.now().strftime('%Y%m%d %H:%M:%S')}
		return data
				
				
	def send(self):
		data = {'data': self.peer_id()}
		self.sendMessage(data)
		
	def receiveMessageCallback(self, msg):
		self.m_peers[msg['id']] = msg

	def ping_answer(self, peer, answer, connected=False):
		Log.info('ping - connecting', connected, answer)
		if connected:
			peer['last-update'] = datetime.now()
		else:				     
			self.m_ipfs_gateway.connect(peer['link'], lambda x: self.ping_answer(peer, x, True))
	
	def ping(self):
		if (self.m_server_is_standalone):
			return

		Log.info('ping - peers', self.m_peers)
		if not(self.m_peers):
			return
		self.m_sequence_nr += 1
		peers = [peer for peer in self.m_peers.values()]
		peer = peers[self.m_sequence_nr % len(peers)]

		Log.info('ping - send ping to peer', peer['ping-hash'])		       
		self.m_ipfs_gateway.retrieveDocumentFromHash(peer['ping-hash'], lambda x: self.ping_answer(peer, x))

	def flush(self):
		self.write_peers()


