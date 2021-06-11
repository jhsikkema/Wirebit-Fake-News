"""
	Copyright Sikkema Software 2017. 
	No liabilities or rights can be derived from the correct working of 
	this software or.
"""
import os, os.path
import xml.etree.ElementTree as ElementTree

class Config(object):
	def __init__(self, path):
		if not path is None:
			tree = ElementTree.parse(path).getroot()
			self.m_tree = tree
		else:
			self.m_tree = None

	def __enter__(self):
		return self
		
	def __exit__(self, type, value, traceback):
		pass
			
	def getNodes(self, tags):
		nodes = [ self.m_tree ]
		for tag in tags:
			nodes = [ child for node in nodes for child in node if child.tag == tag]
		configs = [ ]
		for node in nodes:
			conf = Config(None)
			conf.m_tree = node
			configs.append(conf)
		return configs
	
	def path(self, tags):
		return os.path.join(*self[tags].split('/'))


	def __getitem__(self, tags):
		nodes = [ self.m_tree ]
		for tag in tags:
			nodes = [ child for node in nodes for child in node if child.tag == tag]
		if len(nodes)==1:
			return nodes[0].text.strip()
		else:
			return [ node.text.strip() for node in nodes ]

	def __contains__(self, tags):
		assert(isinstance(tags, list) or isinstance(tags, tuple))
		return len(self.__getitem__(tags)) > 0
	
	@property
	def text(self):
		return self.m_tree.text