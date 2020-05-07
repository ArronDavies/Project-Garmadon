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
zone_info = config['ZONE']


class ZoneServer(Server):
	def __init__(self, zone_id, port):
		super().__init__(address=(zone_info['Bindip'], port), max_connections=int(32), incoming_password=b"3.25 ND1", ssl=None)
		self._packets = {}
		self._dispatcher.add_listener(Message.NewIncomingConnection, self._on_conn)
		self._dispatcher.add_listener(Message.UserPacket, self._on_lu_packet)

		self._packets["53-00-00-00"] = Packets.Incoming.VERSION_CONFIRM.VERSION_CONFIRM
		self._packets["53-04-00-01"] = Packets.Incoming.CLIENT_VALIDATION.CLIENT_VALIDATION
		self._packets["53-04-00-13"] = Packets.Incoming.CLIENT_LEVEL_LOAD_COMPLETE.CLIENT_LEVEL_LOAD_COMPLETE
		self._connections = {}
		self.zone_id = zone_id

		ip = requests.get('https://api.ipify.org').text
		create_zone_instance(zone_id=zone_id, ip=ip, port=port)
		print("[ZONE " + self.zone_id + "]" + "Started")

	def _on_conn(self, data: ReadStream, conn: Connection) -> None:
		print("[ZONE " + self.zone_id + "]" + "New Connection from ", conn.get_address())
		address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		self._connections[uid] = conn
		create_session(ip=conn.get_address()[0], port=conn.get_address()[1])
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
			print("[ZONE " + self.zone_id + "]" + "Received and handled packet: " + identifier)
		except KeyError:
			print("[ZONE " + self.zone_id + "]" + "Unhandled Packet: " + identifier)

	def kick_player(self, UUID):
		conn = self._connections[UUID]
		Packets.Outgoing.DISCONNECT_NOTIFY.DISCONNECT_NOTIFY(conn=conn, disconnect_id=0x0b)
		return True
