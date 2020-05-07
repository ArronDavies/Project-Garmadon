from pyraknet.transports.abc import *
from bitstream import *
from Packets.Outgoing import *
from MasterAPI import *


def CREATE_CHARACTER(stream, conn):
	response = WriteStream()
	CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x04, response=response)

	session = get_session_from_connection(ip=conn.get_address()[0], port=conn.get_address()[0])

	conn.send(response, reliability=Reliability.Reliable)
