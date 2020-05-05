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
auth_info = config['AUTH']


class AuthServer(Server):
	def __init__(self):
		super().__init__(address=(auth_info['Bindip'], int(auth_info['Port'])), max_connections=int(32), incoming_password=b"3.25 ND1", ssl=None)
		self._packets = {}
		self._dispatcher.add_listener(Message.NewIncomingConnection, self._on_conn)
		self._dispatcher.add_listener(Message.UserPacket, self._on_lu_packet)

		self._packets["53-00-00-00"] = Packets.Incoming.VERSION_CONFIRM.VERSION_CONFIRM
		self._packets["53-01-00-00"] = Packets.Incoming.LOGIN_REQUEST.LOGIN_REQUEST
		self._connections = {}
		print("[AUTH] Started")

	def _on_conn(self, data: ReadStream, conn: Connection) -> None:
		print("[AUTH] New Connection from ", conn.get_address())
		address = (str(conn.get_address()[0]), str(conn.get_address()[1]))
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		self._connections[uid] = conn
		create_session(ip=conn.get_address()[0], port=conn.get_address()[1])
		set_session_data_value_from_connection(valuetochange="RCT", newvalue="1", ip=conn.get_address()[0], port=conn.get_address()[1])

	def _on_lu_packet(self, data: bytes, conn: Connection):
		stream = ReadStream(data)
		rpid = 0x53
		rct = stream.read(c_ushort)
		pid = stream.read(c_ulong)
		padding = stream.read(c_ubyte)
		identifier = format(rpid, '02x') + "-" + format(rct, '02x') + "-" + format(padding, '02x') + "-" + format(pid, '02x')

		try:
			self._packets[identifier](stream, conn)
			print("[AUTH] Recieved and handled packet: " + identifier)
		except KeyError:
			print("[AUTH] Unhandled Packet: " + identifier)

	def kick_player(self, UUID):
		conn = self._connections[UUID]
		Packets.Outgoing.DISCONNECT_NOTIFY.DISCONNECT_NOTIFY(conn=conn,disconnect_id=0x0b)
		return True
