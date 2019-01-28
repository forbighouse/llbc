import struct
import time
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

    # def unpack(self, packed):
    #     udp_port = struct.unpack(">H", packed[1])[0]
    #     if packed[2] == '':
    #         tcp_port = udp_port
    #     else:
    #         tcp_port = struct.unpack(">H", packed[2])[0]
    #     return packed[0], udp_port, tcp_port


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

    # def unpack(self, packed):
    #     assert (packed[0] == self.version)
    #     end_point_from = EndPoint.unpack(packed[1])
    #     end_point_to = EndPoint.unpack(packed[2])
    #     timestamp = struct.unpack(">I", packed[3])[0]
    #     return [end_point_from, end_point_to, timestamp]

