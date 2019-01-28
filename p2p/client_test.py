from p2p.server import *

def main():
    my_server = '127.0.0.1'
    server_port = 33334
    id = '1111'
    server = BTPeer(5, server_port, id, my_server)
    server.send_to_peer(id, 1, '1234')

if __name__ == "__main__":
    main()
