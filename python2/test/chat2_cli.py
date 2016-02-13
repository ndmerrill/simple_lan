import os, sys
from multiprocessing import Process, Queue
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import server
import client

print "A simple LAN chat program."

name = raw_input("Enter your name: ")[:16]
cli = client.Client(name, 44242)
servers = cli.get_server_list(timeout=.5)
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

cli.join_server(servers[servers_names[selection_int]][0])

print "Connected"

data = ""
while data != "st":
    data = cli.get_data_raw()

print "Chat started"

while True:
    msg = raw_input("> ").strip()
    data = cli.get_data()
    if data != None:
        print data[0] + ": " + data[1]
    if msg != "":
        cli.send_raw(msg)
