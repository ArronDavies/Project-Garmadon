import Packets.Incoming

from pyraknet.transports.abc import *
from uuid import uuid3, NAMESPACE_DNS
from pyraknet.server import Server
from Types.Session import Session
from pyraknet.messages import *
from bitstream import *
from Logger import *


class Character(Server):
	def __init__(self, bind_ip, port, max_connections, incoming_password, ssl):
		super().__init__(address=(bind_ip, port), max_connections=int(max_connections), incoming_password=incoming_password, ssl=ssl)
		self._dispatcher.add_listener(Message.NewIncomingConnection, self._on_new_conn)
		self._dispatcher.add_listener(Message.UserPacket, self._on_lu_packet)

		self._sessions = {}
		self._packets = {}
		self._register_packets()
		self._rct = 4

		log(LOGGINGLEVEL.CHARACTERDEBUG, " Server Started")

	def _on_new_conn(self, data: ReadStream, conn: Connection) -> None:
		log(LOGGINGLEVEL.CHARACTERDEBUG, (" New Connection from " + conn.get_address()[0] + ":" + str(conn.get_address()[1])))

		session = Session()
		session._ip = conn.get_address()[0]
		session._port = conn.get_address()[1]
		session._connection = conn

		address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
		uid = str(uuid3(NAMESPACE_DNS, str(address)))
		self._sessions[uid] = session

	def _on_lu_packet(self, data: bytes, conn: Connection):
		stream = ReadStream(data); rpid = 0x53; rct = stream.read(c_ushort); pid = stream.read(c_ulong); padding = stream.read(c_ubyte)

		identifier = format(rpid, '02x') + "-" + format(rct, '02x') + "-" + format(padding, '02x') + "-" + format(pid, '02x')
		try:
			self._packets[identifier](stream, conn, self)
			log(LOGGINGLEVEL.CHARACTERDEBUG, " Handled", identifier)
		except KeyError:
			log(LOGGINGLEVEL.CHARACTERDEBUG, " Unhandled", identifier)

	def _register_packets(self):
		self._packets["53-00-00-00"] = Packets.Incoming.VERSION_CONFIRM.VERSION_CONFIRM
		self._packets["53-04-00-01"] = Packets.Incoming.CLIENT_VALIDATION.CLIENT_VALIDATION
		self._packets["53-04-00-02"] = Packets.Incoming.CLIENT_CHARACTER_LIST_REQUEST.CLIENT_CHARACTER_LIST_REQUEST
		self._packets["53-04-00-03"] = Packets.Incoming.CLIENT_CHARACTER_CREATE_REQUEST.CLIENT_CHARACTER_CREATE_REQUEST

	def get_rct(self):
		return self._rct

	def get_session(self, uid):
		return self._sessions[uid]
