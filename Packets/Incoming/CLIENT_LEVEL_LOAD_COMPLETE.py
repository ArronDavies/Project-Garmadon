import Packets.Outgoing


def CLIENT_LEVEL_LOAD_COMPLETE(stream, conn):
	Packets.Outgoing.CREATE_CHARACTER.CREATE_CHARACTER(stream, conn)