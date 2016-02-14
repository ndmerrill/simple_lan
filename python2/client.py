import socket
import ipHelper
import threading

class Client():
	def __init__(self, port):
		self.port = port
		self.connected = False
		self.myIP = ipHelper.getIP()
		self.server_discovery_port = socket.socket(
			socket.AF_INET, socket.SOCK_DGRAM)

	def getServerList(time=2000):
		#  the subnet prefix is the first two elements from the client ip
		#  address.  eg 192.168.
		subnet_prefix = myIP.split(".")[0] + "." + myIP.split(".")[1] + "."

		# this creates a list of /24 subnets to ping
		subnets_24 = [subnet_prefix + i + "." for i in xrange(256)]
		return_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		return_sock.listen(128)

		data = ipHelper.pack_ip()

		threads = []
		for subnet in subnets_24:
			t = threading.Thread(target=self._subnet_poller, ars=(subnet, data))
		    threads.append(t)
		    t.start()

		for t in threads:
			t.join()
		


	def _subnet_poller(target, data):
		"""target is the /24 subnet targeted by this thread and data is the
			data to be sent"""
		for i in xrange(256):
			self.server_discovery_port.sendto(data, (target+i, self.port))

		
