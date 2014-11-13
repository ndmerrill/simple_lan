import socket
import thread
import json


class Server():
    """Server(name, port[, ip=None])
name it sent to all clients requesting a server list. The detection port is
the port that clients will ping while looking for the server.  If it is not
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
            if rec['type'] == "ping":
                conn.send(msg)
                conn.close()

            elif rec["type"] == "join":
                self.players[rec['name']] = conn
                player_count += 1
        return player_count

    def receive_from_all(self):
        """Receives data from all of the connected clients"""
        results = {}
        threads = []
        for name in self.players.keys():
            th = Thread(
                target=self._recieve_from_player, args=(name, results)
                )
            th.start()
            threads.append(th)
        for t in threads:
            t.join()
        return results

    def _receive_from_player(self, name, results):
        """
        Receives data from an individual player. Intended for internal use only
        """
        conn = self.players[name]
        data = json.loads(conn.recv(2048))
        results[name] = data
        return data

    def send_to_all(self, data):
        """sends an array or dictionary to all of the connected clients"""
        msg = json.dumps(data)

        for conn in self.players.values():
            conn.send(msg)

    def send_to(self, data, name):
        """
        Like send_to_all, but only sends to a single player
        """
        msg = json.dumps(data)
        self.players[name].send(msg)

    def close_server(self):
        """
        Closes the server object.  It will stop working after this is called
        """
        for conn in self.players.values():
            conn.close()

        






            
        