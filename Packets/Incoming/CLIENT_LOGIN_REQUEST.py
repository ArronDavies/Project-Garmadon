import Packets.Outgoing


# This packet gets sent when Client pressed play

def CLIENT_LOGIN_REQUEST(stream, conn, server):
	Packets.Outgoing.TRANSFER_TO_WORLD.TRANSFER_TO_WORLD(stream, conn, server)
