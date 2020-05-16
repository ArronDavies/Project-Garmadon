import Packets.Incoming
import Packets.Outgoing
from uuid import uuid3, NAMESPACE_DNS
from pyraknet.server import Server
from pyraknet.replicamanager import Replica, ReplicaManager
from Types.Session import Session
from pyraknet.transports.raknet.connection import *
from bitstream import *
from Logger import *
from Types.LWOOBJID import LWOOBJID


class Zone(Server):
	def __init__(self, bind_ip, port, max_connections, incoming_password, ssl, zone_id):
		super().__init__(address=(bind_ip, port), max_connections=int(max_connections), incoming_password=incoming_password, ssl=ssl)
		self._dispatcher.add_listener(Message.NewIncomingConnection, self._on_new_conn)
		self._dispatcher.add_listener(Message.UserPacket, self._on_lu_packet)
		self._dispatcher.add_listener(ConnectionEvent.Close, self._on_disconnect)

		self._sessions = {}
		self._packets = {}
		self._register_packets()
		self._rct = 4
		self._rep_man = ReplicaManager(dispatcher=self._dispatcher)
		self.zone_id = str(zone_id)

		log(LOGGINGLEVEL.WORLD, " [" + self.zone_id + "] Server Started")

	def _on_new_conn(self, data: ReadStream, conn: Connection) -> None:
		log(LOGGINGLEVEL.WORLD, (" [" + self.zone_id + "] New Connection from: " + conn.get_address()[0] + ":" + str(conn.get_address()[1])))

		session = Session()
		session.ip = conn.get_address()[0]
		session.port = conn.get_address()[1]
		session.connection = conn
		session.first_validate = True

		address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
		uid = str(uuid3(NAMESPACE_DNS, str(address)))
		self._sessions[uid] = session

	def _on_disconnect(self, address: RaknetConnection) -> None:
		host, port = address.get_address()
		log(LOGGINGLEVEL.WORLD, (" [" + self.zone_id + "] Disconnected " + host + ":" + str(port)))
		addressout = (str(host), int(port))
		uid = str(uuid3(NAMESPACE_DNS, str(addressout)))
		session = self._sessions[uid]
		self._rep_man.destruct(session.current_character.player_object)
		del self._sessions[uid]

	def _on_lu_packet(self, data: bytes, conn: Connection):
		stream = ReadStream(data)
		rpid = 0x53
		rct = stream.read(c_ushort)
		pid = stream.read(c_ulong)
		padding = stream.read(c_ubyte)

		identifier = format(rpid, '02x') + "-" + format(rct, '02x') + "-" + format(padding, '02x') + "-" + format(pid, '02x')
		try:
			if identifier == "53-04-00-15":
				self._packets[identifier](stream, conn, self)
			elif identifier == "53-04-00-05":
				self._packets[identifier](stream, conn, self)
			else:
				self._packets[identifier](stream, conn, self)
				if identifier == "53-04-00-16":
					pass
				else:
					log(LOGGINGLEVEL.WORLDDEBUG, " [" + self.zone_id + "] Handled", identifier)
		except KeyError:
			log(LOGGINGLEVEL.WORLDDEBUG, " [" + self.zone_id + "] Unhandled", identifier)

	def _register_packets(self):
		self._packets["53-00-00-00"] = Packets.Incoming.VERSION_CONFIRM.VERSION_CONFIRM
		self._packets["53-04-00-01"] = Packets.Incoming.CLIENT_VALIDATION.CLIENT_VALIDATION
		self._packets["53-04-00-02"] = Packets.Incoming.CLIENT_CHARACTER_LIST_REQUEST.CLIENT_CHARACTER_LIST_REQUEST
		self._packets["53-04-00-03"] = Packets.Incoming.CLIENT_CHARACTER_CREATE_REQUEST.CLIENT_CHARACTER_CREATE_REQUEST
		self._packets["53-04-00-04"] = Packets.Incoming.CLIENT_LOGIN_REQUEST.CLIENT_LOGIN_REQUEST
		self._packets["53-04-00-05"] = Packets.Incoming.CLIENT_GAME_MSG.CLIENT_GAME_MSG
		self._packets["53-04-00-13"] = Packets.Incoming.CLIENT_LEVEL_LOAD_COMPLETE.CLIENT_LEVEL_LOAD_COMPLETE
		self._packets["53-04-00-15"] = Packets.Incoming.CLIENT_ROUTE_PACKET.CLIENT_ROUTE_PACKET
		self._packets["53-04-00-16"] = Packets.Incoming.CLIENT_POSITION_UPDATE.CLIENT_POSITION_UPDATE

	def get_rct(self):
		return self._rct

	def get_session(self, uid):
		return self._sessions[uid]

	def get_rep_man(self):
		return self._rep_man

	def transfer_world(self, new_world_id, session):
		conn = session.connection
		session.current_character.set_last_zone(new_world_id)
		Packets.Outgoing.TRANSFER_TO_WORLD.TRANSFER_TO_WORLD(stream=None, conn=conn, server=self, is_transfer=True, zone_id=new_world_id)

	def wear_item(self, item_lot, session):
		conn = session.connection
		item_id = LWOOBJID().generate()
		item = {"ItemID": item_id, "IsEquipped": 1, "IsLinked": 1, "Quantity": 1, "ItemLOT": item_lot, "Type": 0}

		session.current_character.inventory.add_item(item_data=item)

		self._rep_man.serialize(session.current_character.player_object, reliability=Reliability.Unreliable)


