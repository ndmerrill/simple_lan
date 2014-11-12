
import sys, time
HOST, PORT = "<broadcast>", 9999
data = " ".join(sys.argv[1:])


#sock.sendto(data + "\n", (HOST, PORT))
#received = sock.recv(1024)

#print "Sent:     {}".format(data)
#print "Received: {}".format(received)


MYPORT = 9999

from socket import *

s = socket(AF_INET, SOCK_DGRAM)
#s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

s.sendto(data, ('<broadcast>', MYPORT))
