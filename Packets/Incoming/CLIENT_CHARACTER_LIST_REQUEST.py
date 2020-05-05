from Packets.Outgoing import *


def CLIENT_CHARACTER_LIST_REQUEST(stream, conn):
	CHARACTER_LIST_RESPONSE.CHARACTER_LIST_RESPONSE(stream, conn)
