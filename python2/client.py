import socket
import ipHelper
import threading
import time
import struct

class Client():
    def __init__(self, name, port):
        self.port = port
        self.name = name
        self.connected = False
        self.myIP = ipHelper.get_ip()
        self.server_discovery_port = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        self.connection = None

    def get_server_list(self, wait_time=1.5):
        #  the subnet prefix is the first two elements from the client ip
        #  address.  eg 192.168.
        subnet_prefix = self.myIP.split(".")[0] + "." + self.myIP.split(".")[1] + "."

        # this creates a list of /24 subnets to ping
        subnets_24 = [subnet_prefix + str(i) + "." for i in xrange(256)]
        return_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_sock.bind((self.myIP, self.port))
        return_sock.setblocking(0)
        return_sock.listen(128)

        data = ipHelper.pack_ip()

        print("i")
        threads = []
        for subnet in subnets_24:
            t = threading.Thread(target=self._subnet_poller, args=(subnet, data))
            threads.append(t)
            t.start()

        print("i")
        for t in threads:
            t.join()

        print("i")
        time.sleep(wait_time)

        out = []

        try:
            while True:
                conn, addr = return_sock.accept()
                data = conn.recv(24)
                conn.close()
                ip = ipHelper.unpack_ip(data[0:4])
                port = struct.unpack("I", data[4:8])[0]
                name = data[8:].strip()
                out.append((ip, port, name))
                print ip, name, port

        except socket.error as msg:
            print(msg)
            pass

        finally:
            try:
                conn.close()
            except :
                pass

        return out

    def _subnet_poller(self, target, data):
        """target is the /24 subnet targeted by this thread and data is the
            data to be sent"""
        print "sends?"
        for i in xrange(256):
            # print("hi" + str(i))

            btime = time.clock()
            try:
                self.server_discovery_port.sendto(data, (target+str(i), self.port))
            except socket.error as msg:
                pass
                # catches permission denied errors and ignores them because it
                # doesn't matter if a couple of ip addresses don't work
            # print("done" + str(i))

            print(time.clock()-btime)
        print("done")

    def join_server(self, ip):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, self.port))

        self.connection.send(self.name.rjust(16))
        data = int(self.connection.recv(1));
        if (data == 1):
            print("server is full")
            return False
        self.connection.setblocking(False)
        self.connected = true

    def get_data_raw(self):
        try:
            p_size = self.connection.recv(2)
            p_size = struct.unpack("!H", p_size)
            data = self.connection.recv(int(p_size[0]))
        except socket.error:
            return None
        return data

    def send_data_raw(self, msg):
        if not self.connected:
            return False
        p_size = len(msg)
        p_size = struct.pack("!H", p_size)
        try:
            self.connection.sendall(p_size)
            self.connection.sendall(msg)
            return True
        except socket.error:
            return False


if __name__ == '__main__':
    c = Client("nathan", 40393)
    l = c.get_server_list()
    print(l)

