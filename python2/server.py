# import socket


# def start_server(port):

    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind(('<broadcast>', port))

    # while True:
        # data, addr = sock.recvfrom(1024)
        # print(data)
# start_server(40393)
# Echo server program

import socket
import ipHelper

HOST = ipHelper.getIp()
PORT = 40393
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    data = s.recv(1024)
    if not data: break
    print(data)

conn.close()
