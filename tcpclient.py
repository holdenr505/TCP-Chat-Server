import socket
import threading
import argparse
from sys import exit
from time import sleep

def sendmessage(name, socket, serveraddress, serverport):
    while True:
        try:
            socket.send('{}: {}'.format(name, input('')).encode())
        except TimeoutError:
            #Attempt to reconnect to the server
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.connect((serveraddress, serverport))
           

def recvmessage(socket):
    while True:
        msg = socket.recv(512)
        print(msg.decode('ascii'))

parser = argparse.ArgumentParser()
parser.add_argument('address', help='Server IP address')
parser.add_argument('port', type=int, help='Port number of server')
parser.add_argument('username', help='Your username')
arguments = parser.parse_args()

while len(arguments.username) < 2 or len(arguments.username) > 9:
    arguments.username = input('Username must be between 2 and 9 characters')

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((arguments.address, arguments.port))
clientsocket.send((str(len(arguments.username)) + arguments.username).encode())

authorizationmsg = clientsocket.recv(2).decode('ascii')

if authorizationmsg == 'OK':
    sendthread = threading.Thread(target=sendmessage, args=((arguments.username, clientsocket, 
                                                             arguments.address, arguments.port,)))
    recvthread = threading.Thread(target=recvmessage, args=((clientsocket,)))

    try:
        sendthread.start()
        recvthread.start()
    except KeyboardInterrupt:
        print('Exiting program and closing socket')
        clientsocket.close()
        exit(0) 
else:
    print('User already exists')