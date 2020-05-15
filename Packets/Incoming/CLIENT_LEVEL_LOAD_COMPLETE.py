import Packets.Outgoing.CREATE_CHARACTER


def CLIENT_LEVEL_LOAD_COMPLETE(stream, conn, server):
	Packets.Outgoing.CREATE_CHARACTER.CREATE_CHARACTER(stream, conn, server)
