from Packets.Outgoing import *
from bitstream import *
from uuid import uuid3, NAMESPACE_DNS
from pyraknet.transports.abc import *


def GET_FRIENDS_LIST_RESPONSE(stream, conn, server):
	address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	uid = str(uuid3(NAMESPACE_DNS, str(address)))
	session = server.get_session(uid)

	response = WriteStream()
	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x1e, response=response)

	response.write(c_ubyte(0))

	friends = WriteStream()
	friends.write(c_ushort(len(session.current_character.friends)))

	for friend in session.current_character.friends:
		friends.write(c_bool(friend.online))
		friends.write(c_bool(friend.best_friend))
		friends.write(c_bool(friend.is_free_to_play))
		friends.write(bytes(0), allocated_length=5)
		friends.write(c_ushort(friend.world_id))
		friends.write(c_ushort(friend.world_instance))
		friends.write(c_ulong(friend.world_clone))
		friends.write(c_longlong(friend.minifig_id))
		friends.write(friend.name, allocated_length=66)
		friends.write(bytes(0), allocated_length=6)

	response.write(c_ushort(95))  # Note: Length of friends
	response.write(bytes(friends))

	conn.send(response, reliability=Reliability.Reliable)
