import socket
import thread
import json

class Client(object):
	"""docstring for Client"""
	def __init__(self, name):
		super(Client, self).__init__()
		self.name = name


	def get_server_list(self):
		broadCastSock = 
		servers = {}

