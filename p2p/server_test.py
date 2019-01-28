from p2p.server import *


if __name__ == "__main__":
    my_endpoint = EndPoint(u'127.0.0.1', 30303, 30303)
    their_endpoint = EndPoint(u'10.3.27.98', 30303, 30303)

    server = PingServer(my_endpoint)

    listen_thread = server.udp_listen()
    listen_thread.start()

    server.ping(their_endpoint)

