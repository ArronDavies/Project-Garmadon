from pyraknet.transports.abc import *
import Packets.Outgoing

from bitstream import *
import os


def VERSION_CONFIRM(stream, conn, server, game_version):
	response = WriteStream()

	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x00, 0x00, response=response)

	if game_version == "171023":
		response.write(c_ulong(171023))
	else:
		response.write(c_ulong(171022))
	response.write(c_ulong(0x93))
	response.write(c_ulong(server.get_rct()))
	response.write(c_ulong(os.getpid()))
	response.write(c_ushort(0xff))
	if game_version == "171023":
		response.write(c_ulong(171023))
	else:
		response.write(c_ulong(171022))
	response.write(str(""), allocated_length=33)

	conn.send(response, reliability=Reliability.Reliable)
