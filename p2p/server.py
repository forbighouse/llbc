from p2p.packet_val import *
import gevent
from xmlrpc.server import SimpleXMLRPCServer
import socket
from gevent import Greenlet
from gevent.event import Event
from gevent.select import select
import struct
import threading
import time
import rlp
import hashlib
import sha3
import struct
from ipaddress import ip_address
import traceback
from p2p.constants import LOGGER, BUCKET_SIZE, K_BOND_EXPIRATION, K_EXPIRATION, K_MAX_NEIGHBORS, K_REQUEST_TIMEOUT

# class Pending(Greenlet):
#
#     def __init__(self, node, packet_type, callback, timeout=K_REQUEST_TIMEOUT):


class Server(object):
    def __init__(self, boot_nodes):
        self.end_point = EndPoint(u'127.0.0.1', 30303, 30303)
        self.boot_nodes = boot_nodes

        self.pending_hold = []
        self.last_pong_received = {}
        self.last_ping_received = {}

        priv_key_file = open('', 'r')
        priv_key_serialized = priv_key_file.read()
        priv_key_file.close()
        # self.priv_key =

        # routing table
        self.table = RoutingTable()

        # initialize udp socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', self.end_point.udp_port))
        self.sock.setblocking(False)

    def add_table(self, node):
        self.table.add_node(node)

    def add_pending(self, pending):
        pending.start()
        self.pending_hold.append(pending)
        return pending

    def run(self):
        gevent.spawm(self.clean_pending)
        gevent.spawn(self.listen)
        evt = Event()
        evt.wait()

    def clean_pending(self):
        while True:
            for pending in list(self.pending_hold):
                if not pending.is_alive:
                    self.pending_hold.remove(pending)
            time.sleep(K_REQUEST_TIMEOUT)

    def listen(self):
        LOGGER.info("{:5} listening...".format(''))
        while True:
            ready = select([self.sock], [], [], 1.0)
            if ready[0]:
                data, addr = self.sock.recvfrom(2048)
                gevent.spawn(self.receive, data, addr)

    def receive(self, data, addr):
        print("In reveive func")
        print("data: ", data)
        print("addr: ", addr)
        pass

    def receive_pong(self, addr, pubkey, pong):
        pass


    def wrap_packet(self, packet):
        # FIXME
        b = rlp.encode(packet.pack())
        payload = packet.packet_type + b
        return payload


    def ping(self, node, callback=None):
        ping = PingNode(self.end_point, node.end_point, time.time())
        message = self.wrap_packet(ping)
        # msg_hash = message[:32]

        def reply_call(chunks):
            if chunks.pop().echo == msg_hash:
                if callback is not None:
                    callback()
                return True

        ep = (node.end_point.address.exploded, node.end_point.udp_port))
        pending = self.add_pending(Pending(node, Pong.packet_type, reply_call))
        print("sending ", str(ping))
        self.sock.sendto(message, ep)

        return pending


class PingServer(object):
    def __init__(self, my_end_point):
        self.end_point = my_end_point
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.end_point.udp_port))


    def udp_listen(self):
        return threading.Thread(target=self.receive)

    def receive(self):
        print("listening...")
        data, addr = self.sock.recvfrom(1024)






