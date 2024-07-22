import socket
import threading
import argparse

def sendmessage(name, socket, serveraddress, serverport):
    socket.send('{}: {}'.format(name, input('')).encode())

def recvmessage(socket):
    while True:
        try:
            msg = socket.recv(512)
            print(msg.decode('ascii'))
        except:
            print('Socket error. Closing connection...')
            socket.close()
            break            

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

#Server will send back a two character authentication code
#"OK" if username available, "NO" if unavailable
authenticationmsg = clientsocket.recv(2).decode('ascii')

if authenticationmsg == 'OK':
    sendthread = threading.Thread(target=sendmessage, args=((arguments.username, clientsocket, 
                                                             arguments.address, arguments.port,)))
    recvthread = threading.Thread(target=recvmessage, args=((clientsocket,)))

    sendthread.start()
    recvthread.start()

else:
    print('User already exists')