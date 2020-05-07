from pyraknet.transports.abc import *
from bitstream import *
from Packets.Outgoing import *



def CHARACTER_RENAME_RESPONSE(stream, conn, responsecode):
	response = WriteStream()
	response.write(c_ubyte(responsecode))
	CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x08, response=response)

	conn.send(response, reliability=Reliability.Reliable)
	CHARACTER_LIST_RESPONSE.CHARACTER_LIST_RESPONSE(stream, conn)
