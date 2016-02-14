import socket
import ipHelper
import struct

HOST = ipHelper.get_ip()
PORT = 40393
NAME = "hello"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    data = s.recv(4)
    connection_ip = ipHelper.unpack_ip(data)
    print(connection_ip)
    connecting = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connecting.connect((connection_ip, PORT))
    connecting.sendall(ipHelper.pack_ip(ipHelper.get_ip()) +
            struct.pack("I", PORT) + NAME.rjust(16))
    connecting.close()

conn.close()
