from uuid import uuid3, NAMESPACE_DNS
from pyraknet.transports.abc import *
from Packets.Outgoing import *
from bitstream import *
from Types.LegoData import LegoData
from GameMessages.Outgoing import *


def CREATE_CHARACTER(stream, conn, server):
	address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	uid = str(uuid3(NAMESPACE_DNS, str(address)))
	session = server.get_session(uid)

	charldf = LegoData()

	charldf.ldf.register_key('accountID', session.account_id, 8)
	charldf.ldf.register_key('chatmode', 0, 1)
	charldf.ldf.register_key('editor_enabled', False, 7)
	charldf.ldf.register_key('editor_level', 0, 1)
	charldf.ldf.register_key('freetrial', False, 7)
	charldf.ldf.register_key('gmlevel', session.current_character.gm_level, 1)
	charldf.ldf.register_key('legoclub', True, 7)

	if session.current_character.last_zone == "0":
		charldf.ldf.register_key('levelid', 1000, 8)
	else:
		charldf.ldf.register_key('levelid', session.current_character.last_zone, 8)

	charldf.ldf.register_key('name', session.current_character.name, 0)
	charldf.ldf.register_key('objid', session.current_character.object_id, 9)
	charldf.ldf.register_key('reputation', session.current_character.reputation, 8)
	charldf.ldf.register_key('template', 1, 1)

	response = WriteStream()
	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x04, response=response)

	response.write(charldf)

	conn.send(response, reliability=Reliability.ReliableOrdered)

	replica_manager = server.get_rep_man()

	session.current_character.create_player_object()
	player_object = session.current_character.player_object

	replica_manager.construct(player_object, new=True, important=True)

	replica_manager.add_participant(conn=conn, server=server)
