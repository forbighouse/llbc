import struct
import binascii
from ipaddress import ip_address


class EndPoint(object):

    def __init__(self, address, udp_port, tcp_port):
        """
        :param address: str bytes
        :param udp_port:
        :param tcp_port:
        """
        if isinstance(address, bytes) and len(address) > 4:
            address = address.decode('utf-8')

        self.address = ip_address(address)
        self.udp_port = udp_port
        self.tcp_port = tcp_port

    def pack(self):
        return [self.address.packed,
                struct.pack(">H", self.udp_port),
                struct.pack(">H", self.tcp_port)]

    @classmethod
    def unpack(cls, packed):
        udp_port = struct.unpack(">H", packed[1])[0]
        if packed[2] == '':
            tcp_port = udp_port
        else:
            tcp_port = struct.unpack(">H", packed[2])[0]
        return cls(packed[0], udp_port, tcp_port)


class PingNode(object):

    packet_type = b'\x01'
    version = b'\x03'

    def __init__(self, end_point_from, end_point_to, timestamp):
        self.end_point_from = end_point_from
        self.end_point_to = end_point_to
        self.timestamp = int(timestamp)

    def pack(self):
        return [self.version,
                self.end_point_from.pack(),
                self.end_point_to.pack(),
                struct.pack(">I", self.timestamp)]

    @classmethod
    def unpack(cls, packed):
        assert (packed[0] == cls.version)
        end_point_from = EndPoint.unpack(packed[1])
        end_point_to = EndPoint.unpack(packed[2])
        timestamp = struct.unpack(">I", packed[3])[0]
        return cls(end_point_from, end_point_to, timestamp)


class Pong(object):
    packet_type = b'\x02'

    def __int__(self, to, echo, timestamp):
        self.to = to
        self.echo = echo
        self.timestamp = timestamp

    def __str__(self):
        return "(Pong " + str(self.to) + " <echo hash=""> " + str(self.timestamp) + ")"

    def pack(self):
        return [self.to.pack(),
                self.echo,
                struct.pack(">I", self.timestamp)]

    @staticmethod
    def unpack(cls, packed):
        udp_port = struct.unpack(">H", packed[1])[0]
        tcp_port = struct.unpack(">H", packed[2])[0]
        return cls(packed[0], udp_port, tcp_port)


class FindNeighbors(object):
    packet_type = '\x03'

    def __int__(self, target, timestamp):
        self.target = target
        self.timestamp = timestamp

    def pack(self):
        return [self.target,
                struct.pack(">I", self.timestamp)]

    @classmethod
    def unpack(cls, packed):
        timestamp = struct.unpack(">I", packed[1])[0]
        return cls(packed[0], timestamp)


class Neighbors(object):
    packet_type = '\x04'

    def __init__(self, nodes, timestamp):
        self.nodes = nodes
        self.timestamp = timestamp

    def __str__(self):
        return "(Ns [" + ", ".join(map(str, self.nodes)) + "] " + str(self.timestamp) + ")"

    def pack(self):
        return [
            map(lambda x: x.pack(), self.nodes),
            struct.pack(">I", self.timestamp)
        ]

    @classmethod
    def unpack(cls, packed):
        nodes = map(lambda x: Node.unpack(x), packed[0])
        timestamp = struct.unpack(">I", packed[1])[0]
        return cls(nodes, timestamp)


class Node(object):

    def __init__(self, endpoint, node_key):
        self.endpoint = endpoint
        self.node_key = None
        self.node_id = None
        self.added_time = Node

        self.set_pubkey(node_key)

    def set_pubkey(self, pubkey):
        self.node_key = pubkey
        self.node_id = 'test'

    def __str__(self):
        return "(N " + binascii.b2a_hex(self.node_id)[:8] + ")"

    def pack(self):
        packed = self.endpoint.pack()
        packed.append(self.node_key)
        return packed

    @classmethod
    def unpack(cls, packed):
        endpoint = EndPoint.unpack(packed[0:3])
        return cls(endpoint, packed[3])
