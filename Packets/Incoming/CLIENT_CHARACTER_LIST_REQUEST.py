from bitstream import *
from Packets.Outgoing import *
from uuid import uuid3, uuid4, NAMESPACE_DNS


def CLIENT_CHARACTER_LIST_REQUEST(stream, conn, server):
	address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	uid = str(uuid3(NAMESPACE_DNS, str(address)))
	session = server.get_session(uid)

	CHARACTER_LIST_RESPONSE.CHARACTER_LIST_RESPONSE(stream, conn, server)
