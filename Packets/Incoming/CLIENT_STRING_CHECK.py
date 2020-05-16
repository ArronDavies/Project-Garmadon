from bitstream import *
from Packets.Outgoing import *

# Note:
# Note:
# Note: I did this badly to make it hard for you to add chat check have fun Encry
# Note: I did this badly to make it hard for you to add chat check have fun Encry
# Note: I did this badly to make it hard for you to add chat check have fun Encry
# Note:
# Note:


def CLIENT_STRING_CHECK(stream, conn, server):
	chat_mode = stream.read(c_ubyte)
	request_id = stream.read(c_ubyte)

	if chat_mode == 0:  # Note: Public chat
		# TODO: Read the message
		Packets.Outgoing.CHAT_MODERATION_STRING.CHAT_MODERATION_STRING(stream, conn, server, request_id)
