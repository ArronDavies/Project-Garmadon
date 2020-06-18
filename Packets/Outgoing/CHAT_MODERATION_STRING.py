from Packets.Outgoing import *
from bitstream import *
from pyraknet.transports.abc import *
import better_profanity


# Note:
# Note:
# Note: I did this badly to make it hard for you to add chat check have fun Encry
# Note: I did this badly to make it hard for you to add chat check have fun Encry
# Note: I did this badly to make it hard for you to add chat check have fun Encry
# Note:
# Note:


def CHAT_MODERATION_STRING(stream, conn, server, request_id, message):
	response = WriteStream()
	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x3b, response=response)

	if better_profanity.profanity.contains_profanity(str(message, 'latin1')):
		response.write(c_ubyte(0))
		response.write(c_ushort(0))
		response.write(c_ubyte(request_id))
	else:
		response.write(c_ubyte(1))
		response.write(c_ushort(0))
		response.write(c_ubyte(request_id))

	conn.send(response, reliability=Reliability.Reliable)
