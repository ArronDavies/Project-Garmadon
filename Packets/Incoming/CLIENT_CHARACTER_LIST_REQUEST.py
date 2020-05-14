from Packets.Outgoing import *


def CLIENT_CHARACTER_LIST_REQUEST(stream, conn, server):
	CHARACTER_LIST_RESPONSE.CHARACTER_LIST_RESPONSE(stream, conn, server)
