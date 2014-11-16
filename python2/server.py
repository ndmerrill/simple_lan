import socket
import thread
import json
import Queue
import SocketServer
import struct


class UDPDetectionHandler(SocketServer.BaseRequestHandler):
    """
    This class handles server detection pings over the broadcast thingy.
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        print data
        socket.sendto(data.upper(), self.client_address)


class Server(object):
    """Server(name, port[, ip=])
the name is sent to all clients requesting a server list. The detection port
is the port that clients will ping while looking for the server.  If it is not
set, it will default to the same port that the app will be running on.
"""
    def __init__(self, name, port, timeout, detection_port=None, ip=None):
        self.running_port = port

        self.detection_port = detection_port
        if detection_port is None:
            self.detection_port = port
        self.name = name
        self.timeout = timeout
        if ip == None:
            ip = socket.gethostbyname(socket.gethostname())

        self.ip = ip
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        # except socket.error , msg:
    # print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        self.socket = s
        self.players = {}

    def open_loby(max_players, timeout):
        """
        open_loby(max_players, max_wait_time) -> waits until either
        max_players have joined or it times out
        """

        this.s.listen(max_players*2) 
        # ^ this limits how many conection it will keep queued up and might
        #       need to be changed later
        player_count = 0
        t_initial = time.clock()

        msg = json.dumps({"name":name, "ip":self.ip})

        while player_count < max_players and time.clock()-t_initial < timeout:
            conn, addr = s.accept()
            rec = json.loads(conn.recv(512))
            if rec['type'] == "ping":
                conn.send(msg)
                conn.close()

            elif rec["type"] == "join":
                self.players[rec['name']] = conn
                player_count += 1
        return player_count

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
        data = conn.recv(2)
        p_size = struct.unpack("!H", data)
        data = conn.recv(p_size)
        return data

    def receive_from(self, name):
        """Receives a list or dictionary from a player"""
        return json.loads(self.receive_from_raw(name))

    def send_to_all(self, data):
        """Sends an array or dictionary to all of the connected clients"""
        msg = json.dumps(data)
        self.send_to_all_raw(msg)

    def send_to_all_raw(self, msg):
        """Sends a string of bytes to all of the connected clients"""
        for name in self.players.keys():
            self.send_to_raw(name, msg)

    def send_to(self, name, data):
        """
        Like send_to_all, but only sends to a single player
        """
        msg = json.dumps(data)
        self.send_to_raw(msg, name)

    def send_to_raw(self, name, msg):
        """
        Like send_to_all_raw, but only sends to a single player
        """
        p_size = len(msg)
        p_size = struct.pack("!H", p_size)
        self.sock.send(p_size)
        self.players[name].send(msg)

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
        gws = netifaces.gateways()
        return gws['default'][netifaces.AF_INET][0]




