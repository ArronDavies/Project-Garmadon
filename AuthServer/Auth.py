import Packets.Incoming
from pyraknet.transports.raknet.connection import *
from pyraknet.transports.abc import *
from uuid import uuid3, NAMESPACE_DNS
from pyraknet.server import Server
from Types.Session import Session
from pyraknet.messages import *
from bitstream import *
from Logger import *


class Auth(Server):
    def __init__(self, bind_ip, port, max_connections, incoming_password, ssl):
        super().__init__(address=(bind_ip, port), max_connections=int(max_connections),
                         incoming_password=incoming_password, ssl=ssl)
        self._dispatcher.add_listener(Message.NewIncomingConnection, self._on_new_conn)
        self._dispatcher.add_listener(Message.UserPacket, self._on_lu_packet)
        self._dispatcher.add_listener(ConnectionEvent.Close, self._on_disconnect)

        self._sessions = {}
        self._packets = {}
        self._register_packets()
        self._rct = 1

        log(LOGGINGLEVEL.AUTH, " Server Started")

    def _on_new_conn(self, data: ReadStream, conn: Connection) -> None:
        log(LOGGINGLEVEL.AUTH, (" New Connection from " + conn.get_address()[0] + ":" + str(conn.get_address()[1])))

        session = Session()
        session.ip = conn.get_address()[0]
        session.port = conn.get_address()[1]
        session.connection = conn

        address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
        uid = str(uuid3(NAMESPACE_DNS, str(address)))
        self._sessions[uid] = session

    def _on_disconnect(self, address: RaknetConnection) -> None:
        host, port = address.get_address()
        log(LOGGINGLEVEL.AUTH, (" Disconnected " + host + ":" + str(port)))

        addressout = (str(host), int(port))
        uid = str(uuid3(NAMESPACE_DNS, str(addressout)))

        del self._sessions[uid]

    def _on_lu_packet(self, data: bytes, conn: Connection):
        stream = ReadStream(data);
        rpid = 0x53;
        rct = stream.read(c_ushort);
        pid = stream.read(c_ulong);
        padding = stream.read(c_ubyte)

        identifier = format(rpid, '02x') + "-" + format(rct, '02x') + "-" + format(padding, '02x') + "-" + format(pid,
                                                                                                                  '02x')
        try:
            self._packets[identifier](stream, conn, self)
            log(LOGGINGLEVEL.AUTHDEBUG, " Handled", identifier)
        except KeyError:
            log(LOGGINGLEVEL.AUTHDEBUG, " Unhandled", identifier)

    def _register_packets(self):
        self._packets["53-00-00-00"] = Packets.Incoming.VERSION_CONFIRM.VERSION_CONFIRM
        self._packets["53-01-00-00"] = Packets.Incoming.LOGIN_REQUEST.LOGIN_REQUEST

    def get_rct(self):
        return self._rct

    def get_session(self, uid):
        return self._sessions[uid]
