from pyraknet.transports.abc import *
import Packets.Outgoing
from bitstream import *
from MasterAPI import *
import os


def VERSION_CONFIRM(stream, conn):
	session = get_session_from_connection(ip=conn.get_address()[0], port=conn.get_address()[1])
	response = WriteStream()

	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x00, 0x00, response=response)

	response.write(c_ulong(171022))
	response.write(c_ulong(0x93))
	response.write(c_ulong(int(session['RCT'])))
	response.write(c_ulong(os.getpid()))
	response.write(c_ushort(0xff))
	response.write(c_ulong(171022))
	response.write(str(""), allocated_length=33)

	conn.send(response, reliability=Reliability.Reliable)
