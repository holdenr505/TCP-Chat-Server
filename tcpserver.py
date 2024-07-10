import socket
import threading
import argparse
from sys import exit
from time import sleep

def addClient(clientname, clientsocket, clientdict):
    try:
        if clientname in clientdict:
            clientsocket.send('NO'.encode())
            clientsocket.close()
        else:
            clientsocket.send('OK'.encode())
            clientdict[clientname] = clientsocket
    except TimeoutError:
        clientsocket.close()

    return clientname

def removeClient(clientdict, clientname):
    if clientdict[clientname]:
        clientdict.pop(clientname)

    return clientname

def handleClient(clientsocket, clientname):
    while True:
        try:
            msg = clientsocket.recv(512).decode('ascii')
            broadcast(msg, clients)
        except:
            print("Lost connection with user {}".format(clientname))
            removeClient(clients, clientname)
            broadcast('{} left the server'.format(clientname), clients)
            
def broadcast(msg, clientdict):
    for client in clientdict.values():
        try:
            client.send(msg.encode())
        except TimeoutError:
            client.close()

parser = argparse.ArgumentParser()
parser.add_argument('port', type=int, help='Port number to bind server to')
arguments = parser.parse_args()

clients = {}

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('127.0.0.1', arguments.port))
serversocket.listen(5)

while True:
    try:
        clientconnection, clientaddr = serversocket.accept()
        namelength = clientconnection.recv(1).decode('ascii')
        username = clientconnection.recv(int(namelength)).decode('ascii')
        addClient(username, clientconnection, clients)
        broadcast('{} connected to the server'.format(username), clients)
        handlethread = threading.Thread(target=handleClient, args=(clientconnection, username))
        handlethread.start()
    except KeyboardInterrupt:
        print('\nExiting program and closing socket')
        serversocket.close()
        exit(0)