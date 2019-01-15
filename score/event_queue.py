from socket import *
from time import ctime

def server_node():
    HOST = ''
    PORT = 10521
    ADDR = (HOST, PORT)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(5)
    while True:
        print('Waiting )


