import Packets.Incoming
import Packets.Outgoing
from pyraknet.transports.abc import *
from uuid import uuid3, NAMESPACE_DNS
from pyraknet.server import Server
from Types.Session import Session
from pyraknet.messages import *
from bitstream import *
from Logger import *

class Zone(Server):
    def __init__(self, bind_ip, port, max_connections, incoming_password, ssl):
        super().__init__(address=(bind_ip, port), max_connections=int(max_connections), incoming_password=incoming_password, ssl=ssl)

        self._dispatcher.add_listener(Message.UserPacket, self._on_lu_packet)
        self._dispatcher.add_listener(Message.NewIncomingConnection, self._on_new_connection)

        self._packets = {}
        self._register_packets()

        #self._replica_manager = ReplicaManager(dispatcher=self._dispatcher)

        log(LOGGINGLEVEL.WORLDDEBUG, " Server Started")

    def _on_new_connection(self, data: ReadStream, conn: Connection) -> None:
        session = self.master.get_session(connection=conn.get_address())
        session.set_server_state(state=2)  # 0 = Auth, 1 = Char, 2 = Zone/World
        log(LOGGINGLEVEL.WORLDDEBUG, " New Connection from ", conn.get_address())

    def _on_lu_packet(self, data: bytes, conn: Connection):
        stream = ReadStream(data)
        rpid = 0x53
        rct = stream.read(c_ushort)
        pid = stream.read(c_ulong)
        padding = stream.read(c_ubyte)
        identifier = format(rpid, '02x') + "-" + format(rct, '02x') + "-" + format(padding, '02x') + "-" + format(pid,
                                                                                                                  '02x')

        try:
            self._packets[identifier](stream, conn, self.master)
            log(LOGGINGLEVEL.WORLDDEBUG, " Recieved and handled packet: " + identifier)
        except KeyError:
            log(LOGGINGLEVEL.WORLDDEBUG, " Unhandled Packet: " + identifier)

    def _register_packets(self):
        self._packets["53-00-00-00"] = Packets.Incoming.VERSION_CONFIRM.VERSION_CONFIRM
        self._packets["53-04-00-01"] = Packets.Incoming.CLIENT_VALIDATION.CLIENT_VALIDATION
        self._packets["53-04-00-02"] = Packets.Incoming.CLIENT_CHARACTER_LIST_REQUEST.CLIENT_CHARACTER_LIST_REQUEST
        self._packets["53-04-00-03"] = Packets.Incoming.CLIENT_CHARACTER_CREATE_REQUEST.CLIENT_CHARACTER_CREATE_REQUEST
        self._packets["53-04-00-04"] = Packets.Incoming.LOGIN_REQUEST.LOGIN_REQUEST
        #self._packets["53-04-00-05"] = CLIENT_GAME_MSG.CLIENT_GAME_MSG
        #self._packets["53-04-00-06"] = CLIENT_CHARACTER_DELETE_REQUEST.CLIENT_CHARACTER_DELETE_REQUEST
        #self._packets["53-04-00-07"] = CLIENT_CHARACTER_RENAME_REQUEST.CLIENT_CHARACTER_RENAME_REQUEST
        #self._packets["53-04-00-13"] = CLIENT_LEVEL_LOAD_COMPLETE.CLIENT_LEVEL_LOAD_COMPLETE

    def get_replica_manager(self):
        return self._replica_manager

    def _load_objects(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        luz = config['LUZMAPFILES']
        luz_path = luz[self.zone_id]
        with open(luz_path, "rb") as file:
            data = file.read()
            luz_len = len(data)
            stream = ReadStream(data, unlocked=True)

        version = stream.read(c_ulong)
        if version >= 36:
            versioncontrol = stream.read(c_ulong)
        world_id = stream.read(c_uint)
        if version >= 38:
            spawn_pos = stream.read(c_float), stream.read(c_float), stream.read(c_float)
            spawn_rot = stream.read(c_float), stream.read(c_float), stream.read(c_float), stream.read(c_float)
        if version < 37:
            scenecount = stream.read(c_ubyte)
        elif version >= 37:
            scenecount = stream.read(c_ulong)


#class ReplicaManager:
#    def __init__(self, dispatcher: EventDispatcher):
#        self._dispatcher = dispatcher
#        self._dispatcher.add_listener(ConnectionEvent.Close, self._on_conn_close)
#        self._participants: Set[Connection] = set()
#        self._network_ids: Dict[Replica, int] = {}
#        self._current_network_id = 0
#
##    def add_participant(self, conn: Connection) -> None:
#        print("[ReplicaManager] added connection: ", conn.get_address()[0])
#        self._participants.add(conn)
#        for obj in self._network_ids:
#            self._construct(obj, new=False, recipients=[conn])
#
#    def construct(self, obj: Replica, new: bool = True) -> None:
#        """
#        Send a construction message to participants.
#
#        The object is registered and participants joining later will also receive a construction message when they join (if the object hasn't been destructed in the meantime).
#        The actual content of the construction message is determined by the object's write_construction method.
#        """
        self._construct(obj, new)
#
#    def _construct(self, obj: Replica, new: bool = True, recipients: Iterable[Connection] = None) -> None:
#        if recipients is None:
#            recipients = self._participants
#
#        if new:
#            self._network_ids[obj] = self._current_network_id
#            self._current_network_id += 1
#
#        out = WriteStream()
#        out.write(c_ubyte(Message.ReplicaManagerConstruction.value))
#        out.write(c_bit(True))
#        out.write(c_ushort(self._network_ids[obj]))
#        obj.write_construction(out)

#        out = bytes(out)

#        for conn in recipients:
#            conn.send(out)

#    def serialize(self, obj: Replica) -> None:
#        """
#        Send a serialization message to participants.
#
#        The actual content of the serialization message is determined by the object's serialize method.
#        Note that the manager does not automatically send a serialization message when some part of your object changes - you have to call this function explicitly.
#        """
#        out = WriteStream()
#        out.write(c_ubyte(Message.ReplicaManagerSerialize.value))
#        out.write(c_ushort(self._network_ids[obj]))
#        obj.serialize(out)

#        out = bytes(out)
#        for conn in self._participants:
#            conn.send(out, reliability=Reliability.Reliable)

#    def destruct(self, obj: Replica) -> None:
#        """
#        Send a destruction message to participants.
#
#        Before the message is actually sent, the object's on_destruction method is called.
#        This message also deregisters the object from the manager so that it won't be broadcast afterwards.
#        """
#        log.debug("destructing %s", obj)
#        obj.on_destruction()
#        out = WriteStream()
#        out.write(c_ubyte(Message.ReplicaManagerDestruction.value))
#        out.write(c_ushort(self._network_ids[obj]))
#
#        out = bytes(out)
#        for conn in self._participants:
#            conn.send(out)
#
#        del self._network_ids[obj]
#
    def _on_conn_close(self, conn: Connection) -> None:
        self._participants.discard(conn)