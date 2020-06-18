import Packets.Outgoing.CREATE_CHARACTER


# This packet is the packet that notifies the server that it has loaded a world

def CLIENT_LEVEL_LOAD_COMPLETE(stream, conn, server):
	Packets.Outgoing.CREATE_CHARACTER.CREATE_CHARACTER(stream, conn, server)
