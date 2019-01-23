
from p2p.server import *



if __name__ == "__main__":
    my_server = '127.0.0.1'
    server_port = 33333
    id = '1111'
    server = BTPeer(5, server_port, id, my_server)
    server.main_loop()


