from bitstream import *
from Packets.Outgoing import CONSTRUCT_PACKET_HEADER


def ServerDoneLoadingAllObjects(objid, message_id):
	response = WriteStream()
	CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x0c, response=response)
	response.write(c_longlong(objid))
	response.write(c_ushort(message_id))

	return response
