import os, sys
from multiprocessing import Process, Queue, Pool
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import server
import client

PORT = 40393

def get_input(cli, pipe):
    while True:
        if pipe.poll():
            message = pipe.recv()
            cli.send_raw(message)
            print("sent message '" + message + "'")
        data = cli.get_data_raw()
        if data != None:
            print(data)


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
    parent, child = Pipe()
    p = Process(target=get_input, args=(cli, child,))
    p.start()

    a = raw_input("> ").strip()
    while a:
        parent.send(a)
        a = raw_input("> ").strip()
    p.join()

else:
    name = raw_input("Enter the name of your server: ")[:16]
    serv = server.Server(name, 40393)
    serv.open_lobby()
    raw_input()
    serv.close_lobby()

    while True:
        data = serv.receive_from_all_raw()
        for a in data.keys():
            if data[a] != None:
                serv.send_to_all_raw(data[a])
