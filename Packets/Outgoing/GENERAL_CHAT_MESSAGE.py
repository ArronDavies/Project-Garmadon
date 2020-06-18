from bitstream import *
from Packets.Outgoing import *
from pyraknet.transports.abc import *


def GENERAL_CHAT_MESSAGE(stream, conn, server, message, sender_name, sender_objid, is_mythran=False, channel=0x04):
	response = WriteStream()
	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x02, 0x01, response=response)

	response.write(c_ulonglong(0))  # Note: Unknown
	response.write(c_ubyte(channel))  # Note: Public chat
	response.write(c_ubyte(len(message) * 2))
	response.write(bytes(0), allocated_length=3)
	response.write(sender_name, allocated_length=33)
	response.write(c_ulonglong(sender_objid))
	response.write(c_ushort(0))  # Note: Unknown
	response.write(c_bool(is_mythran))
	response.write(message, allocated_length=66)

	conn.send(response, reliability=Reliability.Reliable)
