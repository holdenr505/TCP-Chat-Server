import socket
import threading
import argparse
from sys import exit

#check if user with name is already connected and send
#corresponding authentication code
def addClient(clientname, clientsocket, clientdict):
    if clientname in clientdict:
        clientsocket.send('NO'.encode())
        clientsocket.close()
    else:
        clientsocket.send('OK'.encode())
        clientdict[clientname] = clientsocket

    return clientname

#receive messages from users and broadcast to all connected clients
def handleClient(clientsocket, clientname):
    while True:
        try:
            msg = clientsocket.recv(512).decode('ascii')
            broadcast(msg, clients)
        except:
            print('Lost connection with user {}'.format(clientname))
            clientsocket.close()
            clients.pop(clientname)
            break
 
def broadcast(msg, clientdict):
    for client in clientdict.values():
        client.send(msg.encode())

parser = argparse.ArgumentParser()
parser.add_argument('port', type=int, help='Port number to bind server to')
arguments = parser.parse_args()

clients = {}
threads = []

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
        threads.append(handlethread)
        handlethread.start()
    except KeyboardInterrupt:
        print('\nClosing client connections and server socket')
        for client in clients:
            clients[client].close()
        serversocket.close()
        break