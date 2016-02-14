import socket
import ipHelper
import struct
import Queue
import time
import threading

# HOST = ipHelper.get_ip()
# PORT = 40393
# NAME = "hello"
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind((HOST, PORT))

# while True:
#     data = s.recv(4)
#     connection_ip = ipHelper.unpack_ip(data)
#     print(connection_ip)
#     connecting = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     connecting.connect((connection_ip, PORT))
#     connecting.sendall(ipHelper.pack_ip(ipHelper.get_ip()) +
#             struct.pack("I", PORT) + NAME.rjust(16))
#     connecting.close()

# conn.close()


class Server():
    def __init__(self, port, name):
        self.port = port
        self.ip = ipHelper.get_ip()
        self.name = name
        self.players = {} # ip address -> (name, conn)
        self.player_queue = Queue.Queue()
        self.game_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_sock.setblocking(0)
        self.game_sock.bind((self.ip, port))


    def open_lobby(self, callback=None):
        self.lobby = LobbyWorker(self.player_queue, self.port, self.name,
            self.game_sock, callback)
        self.lobby.start()

    def pull_lobby(self):
        while not self.player_queue.empty():
            player = self.player_queue.get()
            if player:
                print player
            ip = player.pop(0)
            self.players[ip] = players

    def close_lobby(self):
        self.pull_lobby()
        self.lobby.join(timeout=5)

    def shutdown(self):
        self.game_sock.close()


class LobbyWorker(threading.Thread):
    def __init__(self, player_queue, port, name, sock, callback):
        super(LobbyWorker, self).__init__()
        self.q = player_queue
        self.callback = callback
        self.name = name
        self.port = port
        self.stop_request = threading.Event()
        self.game_sock = sock

    def run(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind((ipHelper.get_ip(), self.port))
        # udp_sock.bind((self.ip, self.port))
        # udp_sock.setblocking(0)

        package = ipHelper.pack_ip() + struct.pack("I", self.port) + self.name.rjust(16)

        self.game_sock.listen(5)
        try:   

            while not self.stop_request.isSet():
                try:
                    data = udp_sock.recv(4)
                    print data
                    if data:
                        connection_ip = ipHelper.unpack_ip(data)
                        reply_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        reply_sock.connect((connection_ip, self.port))
                        reply_sock.sendall(package)
                        reply_sock.close()
                except socket.error as msg:
                    print msg
                
                try:
                    conn, addr = self.game_sock.accept()
                    conn.sendall("\x00")
                    name = self.game_sock.recv(16).strip()
                    print addr
                    self.q.put((addr, name, conn))
                except socket.error as msg:
                    # print msg
                    pass
        finally:
            udp_sock.close()
            

    def join(self, timeout=None):
        self.stop_request.set()
        super(LobbyWorker, self).join(timeout)

if __name__ == '__main__':
    s = Server(40393, "deuterium")
    s.open_lobby()
    try:
        for i in xrange(10):
            print s.players.keys()
            s.pull_lobby()
            time.sleep(1)
        s.close_lobby()
        print s.players.keys()
    finally:
        s.close_lobby
    

    s.shutdown()
