from pyraknet.transports.abc import *
from pyraknet.server import Server
from pyraknet.messages import *
from bitstream import *
from MasterAPI import *
import Packets.Incoming
import Packets.Outgoing
import configparser
import uuid

config = configparser.ConfigParser()
config.read('../config.ini')
char_info = config['CHARACTER']


class CharacterServer(Server):
	def __init__(self):
		super().__init__(address=(char_info['Bindip'], int(char_info['Port'])), max_connections=int(32), incoming_password=b"3.25 ND1", ssl=None)
		self._packets = {}
		self._dispatcher.add_listener(Message.NewIncomingConnection, self._on_conn)
		self._dispatcher.add_listener(Message.UserPacket, self._on_lu_packet)

		self._packets["53-00-00-00"] = Packets.Incoming.VERSION_CONFIRM.VERSION_CONFIRM
		self._packets["53-04-00-01"] = Packets.Incoming.CLIENT_VALIDATION.CLIENT_VALIDATION
		self._packets["53-04-00-02"] = Packets.Incoming.CLIENT_CHARACTER_LIST_REQUEST.CLIENT_CHARACTER_LIST_REQUEST
		self._packets["53-04-00-03"] = Packets.Incoming.CLIENT_CHARACTER_CREATE_REQUEST.CLIENT_CHARACTER_CREATE_REQUEST


		self._packets["53-04-00-06"] = Packets.Incoming.CLIENT_CHARACTER_DELETE_REQUEST.CLIENT_CHARACTER_DELETE_REQUEST

		self._connections = {}
		print("[CHARACTER] Started")

	def _on_conn(self, data: ReadStream, conn: Connection) -> None:
		print("[CHARACTER] New Connection from ", conn.get_address())
		address = (str(conn.get_address()[0]), str(conn.get_address()[1]))
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		self._connections[uid] = conn
		set_session_data_value_from_connection(valuetochange="RCT", newvalue="4", ip=conn.get_address()[0], port=conn.get_address()[1])

	def _on_lu_packet(self, data: bytes, conn: Connection):
		stream = ReadStream(data)
		rpid = 0x53
		rct = stream.read(c_ushort)
		pid = stream.read(c_ulong)
		padding = stream.read(c_ubyte)
		identifier = format(rpid, '02x') + "-" + format(rct, '02x') + "-" + format(padding, '02x') + "-" + format(pid, '02x')
		try:
			self._packets[identifier](stream, conn)
			print("[CHARACTER] Recieved and handled packet: " + identifier)
		except KeyError:
			print("[CHARACTER] Unhandled Packet: " + identifier)

	def kick_player(self, UUID):
		conn = self._connections[UUID]
		Packets.Outgoing.DISCONNECT_NOTIFY.DISCONNECT_NOTIFY(conn=conn,disconnect_id=0x0b)
		return True
