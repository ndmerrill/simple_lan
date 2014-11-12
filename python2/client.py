import socket
import thread
import json
import time

class Client(object):
    """docstring for Client"""
    def __init__(self, name, port):
        self.name = name
        self.port = port


    def get_server_list(self, timeout=1):
        """Get's the list of available servers on this port.
        """
        broadcast_sock = socket.socket(AF_INET, SOCK_DGRAM)
        broadcast_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        servers = {}

        for i in xrange(2):
            broadcast_sock.sendto("to", ('<broadcast>', self.port))
            start_time = time.time()
            while (start_time - time.time() < timeout):
                data, address = broadcast_sock.recvfrom(2)
                if data == "fr":
                    servers.append(address)

        return servers


