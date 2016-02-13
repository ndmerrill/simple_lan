import os, sys
from multiprocessing import Process, Queue
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import server

print "A simple LAN chat program."

try:
    name = raw_input("Enter the name of your server: ")[:16]
    serv = server.Server(name, 44242)
    serv.open_lobby(10)

    print "ender d to finish"
    while True:
        a = raw_input("").strip()
        if a == "":
            print "Players joined:", serv.count_lobby(),
        elif a == "d":
            break
    print "out"

    serv.close_lobby()

    serv.send_to_all_raw("st")

    print "opened"

    while True:
        data = serv.receive_from_all_raw()
        for a in data.keys():
            if data[a] != None:
                print a + ": " + data[a]
                serv.send_to_all((a, data[a]))
finally:
    serv.close_lobby()
    print "closed"
