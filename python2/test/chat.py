import os, sys
from multiprocessing import Process, Queue
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
#import server
#import client

print "A simple LAN chat program."

server_or_client = raw_input("Would you like to create a server(c) or join one(j)? ")
while (server_or_client != "c" and server_or_client != "j"):
    server_or_client = raw_input("Please enter either 'j', or 'c': ")

if server_or_client == "j":
    name = raw_input("Enter your name: ")[:16]
    client = Client(name, 44242)
    servers = client.get_server_list()
    print "Servers found:"
    servers_names = servers.keys()
    for server_loc in xrange(len(servers_names)):
        print str(server_loc) + ":", servers_names[server_loc]

    selection = raw_input("Please choose a server by number: ")

    while (True):
        try:
            selection_int = int(selection)
            if (selection_int >=0 and selection_int < len(servers_names)):
                break
        except ValueError:
            pass
        selection = raw_input("Enter a number between 0 and", str(len(servers_names)-1) + ": ")

    client.join_server(servers[servers_names[selection_int]])

    print "Connected"

    data = ""
    while data != "st":
        data = client.get_data_raw()

    print "Chat started"

    while True:
        msg = raw_input("> ")
        # get and update new data from server

def handle_servers(q,server):
    while True:
        data = server.receive_from_all_raw()
        server.send_to_all_raw(data)
        try:
            q.get_nowait()
            break
        except Queue.Empty:
            continue

else:
    name = raw_input("Enter the name of your server: ")[:16]
    server = Server(name, 44242)
    client = Client("host", 44242)
    server.open_lobby()
    try:
        while True:
            print "\rPlayers joined:", server.count_lobby()
    except KeyboardInterrupt:
        pass
    client.join_server(server.ip)
    server.close_lobby()

    server.send_to_all_raw("st")

    data = client.get_data_raw()

    q = Queue()
    p = Process(target=handle_servers, args=(q,server))
    p.start()

    while True:
        ms = raw_input("> ")
        # get and update new data from server

    q.put(1);
    p.join()




