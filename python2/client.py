import socket
import thread
import json
import time
import struct


class Client(object):
    """A client networking object"""
    def __init__(self, name, port):
        assert(len(name) <= 16)
        self.name = name
        self.port = port

    def get_server_list(self, timeout=1):
        """
        Get's the list of available servers on this port.
        """
        broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        servers = {}

        for i in xrange(2):
            broadcast_sock.sendto("to", ('<broadcast>', self.port))
            start_time = time.clock()
            while (time.clock() - start_time < timeout):
                data, address = broadcast_sock.recvfrom(16)

                servers[data.strip()] = address

        return servers

    def join_server(address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, self.port))
        self.sock.sendall(self.name.ljust(16))

    def get_data(self):
        """returns any new data sent from the server"""
        return json.loads(self.get_raw())

    def get_data_raw(self):
        """returns any new data sent from the server"""
        p_size = self.sock.recv(2)
        p_size = struct.unpack("!H", p_size)
        data = self.sock.recv(p_size)
        return data

    def send(self, data):
        """Sends a list or dictionary back to the server"""
        msg = json.dumps(data)
        self.send_raw(msg)

    def send_raw(self, msg):
        """Sends a string of bytes back to the server"""
        p_size = len(msg)
        p_size = struct.pack("!H", p_size)
        self.sock.sendall(p_size)
        self.sock.sendall(msg)
