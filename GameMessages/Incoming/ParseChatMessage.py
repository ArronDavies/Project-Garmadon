from bitstream import *


def ParseChatMessage(stream, conn, server):
	iClientState = stream.read(c_long)
	message_length = stream.read(c_ushort)
	bool = stream.read(c_bool)
