import socket
import ipHelper
import struct
import Queue

HOST = ipHelper.get_ip()
PORT = 40393
NAME = "hello"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    data = s.recv(4)
    connection_ip = ipHelper.unpack_ip(data)
    print(connection_ip)
    connecting = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connecting.connect((connection_ip, PORT))
    connecting.sendall(ipHelper.pack_ip(ipHelper.get_ip()) +
            struct.pack("I", PORT) + NAME.rjust(16))
    connecting.close()

conn.close()


class Server():
	def __init__(self, port, name):
		self.port = port
		self.ip = ipHelper.get_ip()
		self.name = name
		self.players = {} # ip address -> (name, conn)
		self.player_queue = Queue.queue()

	def open_lobby(self, callback=None):
		self.lobby = LobbyWorker(self.player_queue, self.port, self.name,
			callback)

	def pull_lobby(self):
		while not self.player_queue.empty():
			player = self.player_queue.get()
			ip = player.pop(0)
			self.players[ip] = players

	def close_lobby(self);
		self.pull_lobby()
		self.lobby.join()


class LobbyWorker(threading.Thread):
	def __init__(self, player_queue, port, name, callback):
		self.q = player_queue
		self.callback = callback
		self.name = name
		self.port = port
		self.stop_request = threading.Event()

	def run(self):
		udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		udp_sock.bind((ipHelper.get_ip(), self.port))

		while not self.stop_request.isSet():
			pass

	def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)