from bitstream import *
from Packets.Outgoing import *
from pyraknet.transports.abc import *

# Note:
# Note:
# Note: I did this badly to make it hard for you to add chat check have fun Encry
# Note: I did this badly to make it hard for you to add chat check have fun Encry
# Note: I did this badly to make it hard for you to add chat check have fun Encry
# Note:
# Note:


def CHAT_MODERATION_STRING(stream, conn, server, request_id):
	response = WriteStream()
	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x3b, response=response)
	response.write(c_ubyte(1))
	response.write(c_ushort(0))
	response.write(c_ubyte(request_id))

	conn.send(response, reliability=Reliability.Reliable)