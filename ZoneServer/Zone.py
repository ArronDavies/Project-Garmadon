from typing import Iterable

import Packets.Incoming
import Packets.Outgoing
from uuid import uuid3, NAMESPACE_DNS
from Types.Session import Session
from Logger import *
from GameMessages.Outgoing import *
from Utils.LUZReader import LUZReader

from pyraknet.transports.abc import ConnectionEvent, Connection, Reliability
from pyraknet.replicamanager import ReplicaManager, Replica
from pyraknet.transports.raknet.connection import RaknetConnection
from pyraknet.server import Server
from pyraknet.messages import Message
from bitstream import *


class Replica(Replica):
	def __init__(self):
		self.important = True


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
		self._rep_man = CustomReplicaManager(dispatcher=self._dispatcher)

		self.zone_data = None

		self.objects = {}

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

		if not None:
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

	def fly(self, session, filler_argument):
		conn = session.connection

		flight_mode = session.current_character.player_object.components[0]._is_jetpack_in_air

		message = None
		if flight_mode is False:
			session.current_character.player_object.components[0]._is_jetpack_in_air = True
			session.current_character.player_object.components[0]._jetpack_effect = 0xa7
			message = SetJetPackMode.SetJetPackMode(objid=session.current_character.object_id, bypass_checks=True, use=True, effect_id=-1)
		elif flight_mode is True:
			session.current_character.player_object.components[0]._is_jetpack_in_air = False
			session.current_character.player_object.components[0]._jetpack_effect = 0x00
			message = SetJetPackMode.SetJetPackMode(objid=session.current_character.object_id, bypass_checks=False, use=False, effect_id=-1)

		conn.send(message, reliability=Reliability.Unreliable)
		self._rep_man.serialize(session.current_character.player_object, reliability=Reliability.Unreliable)

	def load_objects(self):
		luz = LUZReader(zone_id=self.zone_id)
		luz.parse()
		self.zone_data = luz.zone

		for scene in luz.zone.scenes:
			scene.get_objects()

			for object in scene.objects:
				object.get_components()

				if object.is_constructable:
					object.start(self)
					self.objects[object.objid] = object
				else:
					pass


class CustomReplicaManager(ReplicaManager):
	def add_participant(self, server, conn: Connection) -> None:
		log(LOGGINGLEVEL.REPLICADEBUG, " added connection: " + str(conn.get_address()[0]))
		self._participants.add(conn)

		for obj in self._network_ids:
			if obj.important:
				self._construct(obj, new=False, recipients=[conn])

		address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
		uid = str(uuid3(NAMESPACE_DNS, str(address)))
		session = server.get_session(uid)

		obj_load = ServerDoneLoadingAllObjects.ServerDoneLoadingAllObjects(objid=int(session.current_character.object_id), message_id=0x66a)
		conn.send(obj_load, reliability=Reliability.ReliableOrdered)

		player_ready = PlayerReady.PlayerReady(objid=int(session.current_character.object_id), message_id=0x1fd)
		conn.send(player_ready, reliability=Reliability.ReliableOrdered)

		for obj in self._network_ids:
			if obj.important is not True:
				self._construct(obj, new=False, recipients=[conn], reliability=Reliability.Reliable)

	def serialize(self, obj: Replica, reliability=None) -> None:
		out = WriteStream()
		out.write(c_ubyte(Message.ReplicaManagerSerialize.value))
		out.write(c_ushort(self._network_ids[obj]))
		obj.serialize(out)

		out = bytes(out)
		for conn in self._participants:
			if reliability is not None:
				conn.send(out, reliability=reliability)
			else:
				conn.send(out)

	def construct(self, obj: Replica, new: bool=True, important: bool=False, reliability=None) -> None:
		self._construct(obj, new, important, reliability=None)

	def _construct(self, obj: Replica, new: bool=True, important: bool=False, recipients: Iterable[Connection]=None, reliability=None) -> None:
		# recipients is needed to send replicas to new participants
		if recipients is None:
			recipients = self._participants

		if new:
			self._network_ids[obj] = self._current_network_id
			self._current_network_id += 1

		out = WriteStream()
		out.write(c_ubyte(Message.ReplicaManagerConstruction.value))
		out.write(c_bit(True))
		out.write(c_ushort(self._network_ids[obj]))
		obj.write_construction(out)

		out = bytes(out)
		for conn in recipients:
			if reliability is not None:
				conn.send(out, reliability=reliability)
			else:
				conn.send(out)

