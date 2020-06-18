from uuid import uuid3, uuid4, NAMESPACE_DNS
import configparser
import Packets.Outgoing
from ZoneServer import Zone


# This packet is used to find if the client is the same one handled in auth so no one can access accounts they don't have access too.

def CLIENT_VALIDATION(stream, conn, server):
	username = stream.read(str, allocated_length=33)
	user_key = stream.read(str, allocated_length=33)
	somehashedstring = stream.read(bytes, 32)
	unknown1 = stream.read(bytes, 1)

	address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	uid = str(uuid3(NAMESPACE_DNS, str(address)))
	session = server.get_session(uid)
	session.temp_username = username
	session.sync_account_values_down()
	session.sync_characters_down()

	if user_key == session.session_key:
		if session.first_validate is True:
			Packets.Outgoing.LOAD_STATIC_ZONE.LOAD_STATIC_ZONE(stream, conn, server)
	else:
		Zone.Zone.kick(conn, server)
