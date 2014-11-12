import socket
import thread
import json
import marshal
import socketserver

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
name it sent to all clients requesting a server list. The detection port is
the port that clients will ping while looking for the server.  If it is not
set, it will default to the same port that the app will be running on.
"""
    def __init__(self, name, port, timeout, detection_port=None, ip=None):
        super(Server, self).__init__()
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
        """open_loby(max_players, max_wait_time) -> waits until either
        max_players have joined or it times out
        """
        
        this.s.listen(max_players*2) 
        # ^ this limits how many conection it will keep queued up and might
        # need to be changed later
        player_count = 0
        t_initial = time.clock()

        msg = json.dumps({"name":name, "ip":self.ip})

        while player_count < max_players and time.clock()-t_initial < timeout:
            conn, addr = s.accept()
            rec = json.loads(conn.recv(512))
            if rec['type'] = "ping":
                conn.send(msg)
                conn.close()

            elif rec["type"] = "join":
                self.players[rec['name']] = conn
                player_count += 1
        return player_count




    # def recieve_from_all(self):
    #     results = {}
    #     threads = []
    #     for name in self.players.keys():
    #         th = Thread(
    #             target=self._recieve_from_player, args=(name, results)
    #             )
    #         th.start()
    #         threads.append(th)

    #     map(lambda thread: thread.join(), threads)

    #     for name in results.keys():



    # def _recieve_from_player(self, name, results):
    #     conn = self.players[name]
    #     data = conn.recv(1024)
    #     results[name] = json.loads(data)
        






            
        