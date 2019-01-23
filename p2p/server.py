import socket
import struct
import threading
import time
import traceback


def btdebug(msg):
    print("[%s] %s" % (str(threading.currentThread().getName()), msg))


class BTPeer(object):

    def __init__(self, max_peers, server_port, my_id=None, server_host=None):
        self.debug = True
        self.max_peers = int(max_peers)
        self.server_port = int(server_port)

        if server_host:
            self.server_host = server_host
        else:
            self.__initserver_host()

        if my_id:
            self.my_id = my_id
        else:
            self.my_id = '%s:%d' % (self.server_host, self.server_port)

        self.peers = {}  # 已知peers的列表，内容可以是字典或者哈希表
        self.shutdown = False  # 用来停止主循环

        self.handlers = {}
        self.router = None

    def __initserver_host(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("www.baidu.com", 80))
        self.serverhost = s.getsockname()[0]
        s.close()

    def __debug(self, msg):
        if self.debug:
            btdebug(msg)

    def make_server_socket(self, port, back_log=5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(back_log)
        return s

    def main_loop(self):
        s = self.make_server_socket(self.server_port)
        s.settimeout(2)
        self.__debug('Server started: %s (%s:%d)'
                     % (self.my_id, self.server_host, self.server_port))
        while not self.shutdown:
            try:
                self.__debug('Listening for connections...')
                client_sock, client_addr = s.accept()
                client_sock.settimeout(None)

                t = threading.Thread(target=self.__handle_peer, args=[client_sock])
                t.start()
            except KeyboardInterrupt:
                self.shutdown = True
                continue
            except:
                if self.debug:
                    traceback.print_exc()
                    continue
        self.__debug('Main loop exiting')
        s.close()

    def __handle_peer(self, client_sock):
        self.__debug('Connected' + str(client_sock.getpeername()))

        host, port = client_sock.getpeername()
        peer_conn = BTPeerConnection(None, host, port, client_sock, debug=False)

        try:
            msgtype, msgdata = peer_conn.recvdata()
            if msgtype: msgtype = msgtype.upper()
            if msgtype not in self.handlers:
                self.__debug('Not handled: %s:%s' % (msgtype, msgdata))
            else:
                self.__debug('Handling peer msg: %s, %s' % (msgtype, msgdata))
                self.handlers[msgtype](peer_conn, msgdata)
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
        self.__debug('Disconnecting' + str(client_sock.getpeername()))
        peer_conn.close()

    def sendtopeer(self, peerid, msgtype, msgdata, waitrely=True):
        if self.router:
            nextid, host, port = self.router(peerid)
            if not self.router or not nextid:
                self.__debug('Unable to route %s to %s' % (msgtype, peerid))
                return None
            return self.connect_send(host, port, msgtype, msgdata, pid=nextid, waitrely=waitrely)

    def connect_send(self, host, port, msgtype, msgdata, pid=None, waitrely=True):
        msgreply = []
        try:
            peerconn = BTPeerConnection(pid, host, port, debug=self.debug)
            peerconn.senddata(msgtype, msgdata)
            self.__debug('Sent %s: %s' % (pid, msgtype))

            if waitrely:
                onereply = peerconn.recvdata()
                while (onereply != (None, None)):
                    msgreply.append(onereply)
                    self.__debug('Got reply %s: %s' % (pid, str(msgreply)))
                    onereply = peerconn.recvdata()
                peerconn.close()
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
        return msgreply

    def __run_stabilizer(self, stabilizer, delay):
        while not self.shutdown:
            stabilizer()
            time.sleep(delay)

    def start_stabilizer(self, stabilizer, delay):
        """ Registers and starts a stabilizer function with this peer.
        The function will be activated every <delay> seconds.
        安置者：干啥用的？
        """
        t = threading.Thread(target=self.__run_stabilizer,
                             args=[stabilizer, delay])
        t.start()

    def addhandler(self, msgtype, handler):
        assert len(msgtype) == 4
        self.handlers[msgtype] = handler

    def addrouter(self, router):
        self.router = router

    def addpeer(self, peerid, host, port):
        # 添加peer使list里面的peer与已知peer一致
        if peerid not in self.peers and (self.max_peers == 0 or
                         len(self.peers) < self.max_peers):
            self.peers[peerid] = (host, int(port))
            return True
        else:
            return False

    def getpeer(self, peerid):
        pass

    def removepeer(self, peerid):
        pass

    def addpeerat(self, loc, peerid, host, port):
        pass

    def getpeerat(self, loc):
        pass

    def removepeerat(self, loc):
        pass

    def getpeerids(self):
        pass

    def numberofpeers(self):
        pass

    def maxpeersreached(self):
        pass

    def checklivepeers(self):
        pass


class BTPeerConnection:
    def __init__(self, peer_id, host, port, sock=None, debug=False):
        self.id = peer_id
        self.debug = debug

        if not sock:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, int(port)))
        else:
            self.s = sock
        self.sd = self.s.makefile('rw', 0)

    def __makemsg(self, msgtype, msgdata):
        msglen = len(msgdata)
        msg = struct.pack("!4sL%ds" % msglen, msgtype, msglen, msgdata)
        return msg

    def __debug(self, msg):
        if self.debug:
            btdebug(msg)

    def senddata(self, msgtype, msgdata):
        try:
            msg = self.__makemsg(msgtype, msgdata)
            self.sd.write(msg)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
                return False
        return True

    def recvdata(self):
        try:
            msgtype = self.sd.read(4)
            if not msgtype:
                return (None, None)
            lenstr = self.sd.read(4)
            msglen = int(struct.unpack("!L", lenstr)[0])
            msg = ""
            while len(msg) != msglen:
                data = self.sd.read(min(2048, msglen - len(msg)))
                if not len(data):
                    break
                msg += data

                if len(msg) != msglen:
                    return (None, None)
            return (msgtype, msg)
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
                return (None, None)

    def close(self):
        self.s.close()
        self.s = None
        self.sd = None

    def __str__(self):
        return "|%s|" % self.id

