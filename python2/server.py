import socket
import json
import SocketServer
import struct
import multiprocessing
from multiprocessing import reduction
import netifaces
import Queue
import time


class UDPDetectionHandler(SocketServer.BaseRequestHandler):
    """
    This class handles server detection over UDP broadcast.
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        #print "{} wrote:".format(self.client_address[0])
        #print data
        if data == "to":
            socket.sendto(self.server.server_name.ljust(16), self.client_address)


def UDP_Runner(q,udp_server):
    while True:
        udp_server.handle_request()
        try:
            q.get_nowait()
            break
        except Queue.Empty:
            continue

def lobby_receiver(recv_queue, send_queue, ip, port, max_players, timeout):
    # make a socket for the lobby
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(5)
    sock.setblocking(False)

    try:
        player_count = 0
        t_initial = time.time()

        while player_count < max_players and time.time()-t_initial < timeout:
            try:
                recv_queue.get_nowait()
                break
            except Queue.Empty:
                pass
            try:
                conn, addr = sock.accept()
                rec = conn.recv(16)
                conn.setblocking(False)

                # because you can't pickle a socket object - this is needed
                conn_to_send = reduction.reduce_handle(conn.fileno())

                send_queue.put((rec.strip(), conn_to_send))
                player_count += 1

            except socket.error:
                continue
    finally:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()


class Server(object):
    """Server(name, port[, ip=])
the name is sent to all clients requesting a server list. The detection port
is the port that clients will ping while looking for the server.  If it is not
set, it will default to the same port that the app will be running on.
"""
    def __init__(self, name, port, ip=None):
        self.port = port
        assert(len(name)<=16)
        self.name = name
        if ip == None:
            ip = self._get_computer_ip()
        self.ip = ip
        self.players = {}


    def open_lobby(self, max_players, timeout=604800):
        """
        open_lobby(max_players, max_wait_time) -> waits until either
        max_players have joined or it times out
        """
        # make UDP server
        #print self.ip
        udp_server = SocketServer.UDPServer(
                ('<broadcast>', self.port),
                UDPDetectionHandler)
        udp_server.server_name = self.name # allow broadcast of name
        udp_server.timeout = .05

        # start UDP server in another process

        self.udp_q = multiprocessing.Queue()
        self.udp_p = multiprocessing.Process(target=UDP_Runner, args=(self.udp_q,udp_server))
        self.udp_p.start()


        # make a socket for the loby
        # can we delete this now?
        """
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.bind((self.ip, self.port))
        socket.listen(3)
        socket.setblocking(False)
        player_count = 0
        t_initial = time.time()

        while player_count < max_players and time.time()-t_initial < timeout:
            try:
                conn, addr = socket.accept()
                rec = json.loads(conn.recv(16))
                self.players[rec.strip()] = conn
                player_count += 1

            except socket.error:
                continue
        #until here?"""

        self.send_queue = multiprocessing.Queue()
        self.recv_queue = multiprocessing.Queue()
        self.lobby_process = multiprocessing.Process(
            target=lobby_receiver, args=(self.send_queue, self.recv_queue, self.ip, self.port, max_players, timeout))
        self.lobby_process.start()

    def count_lobby(self):
        """
        Only use while the lobby is open retrieves any new players and returns
        the number of connected players
        """
        while not self.recv_queue.empty():
            name, conn = self.recv_queue.get()
            conn_info = reduction.rebuild_handle(conn)
            conn_usable = socket.fromfd(conn_info, socket.AF_INET, socket.SOCK_STREAM)
            self.players[name] = conn_usable
        return len(self.players.keys())

    def close_lobby(self):
        """
        Closes the lobby and retrieves the player connections
        Returns the number of connected players
        """
        # close UDP server
        self.udp_q.put(1);
        self.udp_p.join()
        self.send_queue.put(1);

        #while not self.recv_queue.empty():
        #    name, conn = self.recv_queue.get()
        #    conn_info = reduction.rebuild_handle(conn)
        #    conn_usable = socket.fromfd(conn_info, socket.AF_INET, socket.SOCK_STREAM)
        #    self.players[name] = conn_usable

        self.lobby_process.join()
        return len(self.players.keys())

    def receive_from_all(self):
        """Receives json data from all of the connected clients"""
        results = {}
        for name in self.players.keys():
            data = self.receive_from(name)
            results[name] = data
        return results

    def receive_from_all_raw(self):
        """Receives raw data from all of the connected clients"""
        results = {}
        for name in self.players.keys():
            data = self.receive_from_raw(name)
            results[name] = data
        return results

    def receive_from_raw(self, name):
        """Receives a string of bytes from a given client"""
        conn = self.players[name]
        try:
            data = conn.recv(2)
            p_size = struct.unpack("!H", data)
            data = conn.recv(p_size)
            return data
        except socket.error:
            return None

    def receive_from(self, name):
        """Receives a list or dictionary from a player"""
        data = self.receive_from_raw(name)
        if data == None:
            return None
        return json.loads(data)

    def send_to_all(self, data):
        """Sends an array or dictionary to all of the connected clients"""
        msg = json.dumps(data)
        return self.send_to_all_raw(msg)

    def send_to_all_raw(self, msg):
        """Sends a string of bytes to all of the connected clients"""
        work = True
        for name in self.players.keys():
            work = work and self.send_to_raw(name, msg)
        return work

    def send_to(self, name, data):
        """Like send_to_all, but only sends to a single player"""
        msg = json.dumps(data)
        return self.send_to_raw(msg, name)

    def send_to_raw(self, name, msg):
        """Like send_to_all_raw, but only sends to a single player"""
        p_size = len(msg)
        p_size = struct.pack("!H", p_size)
        try:
            self.players[name].sendall(p_size)
            self.players[name].sendall(msg)
            return True
        except socket.error:
            return False

    def close_server(self):
        """
        Closes the server object.  It will stop working after this is called
        """
        for conn in self.players.values():
            conn.close()

    def _get_computer_ip(self):
        """
        Returns the ip address of this computer, should be platfrom agnostic
        """
        #gws = netifaces.gateways()
        #return gws['default'][netifaces.AF_INET][0]
        return netifaces.ifaddresses('wlp3s0')[netifaces.AF_INET][0]['addr']




