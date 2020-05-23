import Packets.Incoming
import Packets.Outgoing
from uuid import uuid3, NAMESPACE_DNS
from pyraknet.server import Server
from pyraknet.replicamanager import ReplicaManager
from Types.Session import Session
from pyraknet.transports.raknet.connection import *
from bitstream import *
from Logger import *
from Types.LWOOBJID import LWOOBJID
from GameMessages.Outgoing import *
from Utils.LUZReader import LUZReader
from threading import Thread


class Zone(Server):
	def __init__(self, bind_ip, port, max_connections, incoming_password, ssl, zone_id):
		super().__init__(address=(bind_ip, port), max_connections=int(max_connections), incoming_password=incoming_password, ssl=ssl)
		self.zone_id = str(zone_id)
		self._dispatcher.add_listener(Message.NewIncomingConnection, self._on_new_conn)
		self._dispatcher.add_listener(Message.UserPacket, self._on_lu_packet)
		self._dispatcher.add_listener(ConnectionEvent.Close, self._on_disconnect)

		self._sessions = {}
		self._packets = {}
		self._register_packets()
		self._rct = 4
		self._rep_man = ReplicaManager(dispatcher=self._dispatcher)

		self.zone_data = None

		self.spawners = {}

		self.load_objects()
		self.keep_alive_thread = None

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
		self._packets["53-04-00-19"] = Packets.Incoming.CLIENT_STRING_CHECK.CLIENT_STRING_CHECK
		self._packets["53-04-00-0e"] = Packets.Incoming.CLIENT_GENERAL_CHAT_MESSAGE.CLIENT_GENERAL_CHAT_MESSAGE
		self._packets["53-04-00-1e"] = Packets.Incoming.CLIENT_HANDLE_FUNNESS.CLIENT_HANDLE_FUNNESS

	def get_rct(self):
		return self._rct

	def get_session(self, uid):
		return self._sessions[uid]

	def get_rep_man(self):
		return self._rep_man

	def transfer_world(self, session, args):
		conn = session.connection
		session.current_character.set_last_zone(args[1])
		Packets.Outgoing.TRANSFER_TO_WORLD.TRANSFER_TO_WORLD(stream=None, conn=conn, server=self, is_transfer=True, zone_id=args[1])

	def wear_item(self, session, args):
		conn = session.connection
		item_id = LWOOBJID().generate()
		item = {"ItemID": item_id, "IsEquipped": 1, "IsLinked": 1, "Quantity": 1, "ItemLOT": args[1], "Type": 0}

		session.current_character.inventory.add_item(item_data=item)

		self._rep_man.serialize(session.current_character.player_object, reliability=Reliability.Unreliable)

	def fly(self, session, filler_argument):
		conn = session.connection

		flight_mode = session.current_character.player_object.controllable_physics._is_jetpack_in_air

		message = None
		if flight_mode is False:
			session.current_character.player_object.controllable_physics._is_jetpack_in_air = True
			session.current_character.player_object.controllable_physics._jetpack_effect = 0xa7
			message = SetJetPackMode.SetJetPackMode(objid=session.current_character.object_id, bypass_checks=True, use=True, effect_id=-1)
		elif flight_mode is True:
			session.current_character.player_object.controllable_physics._is_jetpack_in_air = False
			session.current_character.player_object.controllable_physics._jetpack_effect = 0x00
			message = SetJetPackMode.SetJetPackMode(objid=session.current_character.object_id, bypass_checks=False, use=False, effect_id=-1)

		conn.send(message, reliability=Reliability.Unreliable)
		self._rep_man.serialize(session.current_character.player_object, reliability=Reliability.Unreliable)

	def load_objects(self):
		luz = LUZReader(zone_id=self.zone_id)
		luz.parse()
		self.zone_data = luz.zone

		for scene in luz.zone.scenes:
			scene.get_spawners()

			for spawner in scene.spawners:
				spawner.get_components()
				spawner.parse_settings()

				if spawner.is_constructable:
					spawner.start(self)
					self.spawners[spawner.spawner_object_id] = spawner
				else:
					pass

	# 	self.keep_alive_thread = Thread(target=self.keep_alive)
	# 	self.keep_alive_thread.isDaemon = True
	# 	self.keep_alive_thread.start()
	#
	# def keep_alive(self):
	# 	while True:
	# 		for spawner in self.spawners:
	# 			self.spawners[spawner].keep_alive()
	# 		time.sleep(1)