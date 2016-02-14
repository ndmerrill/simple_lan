import os, sys
from multiprocessing import Process, Queue
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import server
import client

PORT = 44242

def get_input():
    return raw_input("> ").strip()

print("A simple LAN chat program.")

server_or_client = raw_input(
        "Would you like to create a server(c) or join one(j)? ")
while (server_or_client != "c" and server_or_client != "j"):
    server_or_client = raw_input("Please enter either 'j', or 'c': ")

if server_or_client == "j":
    name = raw_input("Enter your name: ")[:16]
    cli = client.Client(name, PORT)
    servers = cli.get_server_list()
    print("Servers found:")
    servers_names = servers.keys()
    for server_loc in xrange(len(servers_names)):
        print(str(server_loc) + ":", servers_names[server_loc])

    selection = raw_input("Please choose a server by number: ")

    while (True):
        try:
            selection_int = int(selection)
            if (selection_int >=0 and selection_int < len(servers_names)):
                break
        except ValueError:
            pass
        selection = raw_input("Enter a number between 0 and",
                str(len(servers_names)-1) + ": ")

    cli.join_server(servers[servers_names[selection_int]])

    print("Connected")

    data = ""
    while data != "st":
        data = cli.get_data_raw()

    print("Chat started")

    while True:
        msg = raw_input("> ").strip()
        data = cli.get_data_raw()
        if data != None:
            print(data)
        if msg != "":
            cli.send_raw(msg)

else:
    name = raw_input("Enter the name of your server: ")[:16]
    serv = server.Server(name, 44242)
    cli = client.Client("host", 44242)
    serv.open_lobby(10)
    """try:
        while True:
            #print "\rPlayers joined:", serv.count_lobby(),
            pass
    except KeyboardInterrupt:
        pass"""
    a = raw_input("Say when to stop")
    cli.join_server(serv.ip)
    serv.count_lobby()
    serv.close_lobby()

    serv.send_to_all_raw("st")

    data = cli.get_data_raw()

    while True:
        msg = raw_input("> ").strip()
        data = cli.get_data_raw()
        if data != None:
            print(data)
        if msg != "":
            cli.send_raw(msg)
        data = serv.receive_from_all_raw()
        for a in data.keys():
            if data[a] != None:
                serv.send_to_all_raw(data[a])
