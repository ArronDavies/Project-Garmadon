from pyraknet.transports.abc import *
import Packets.Outgoing
from bitstream import *


def DISCONNECT_NOTIFY(conn, disconnect_id):
	response = WriteStream()

	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x00, 0x01, response=response)

	response.write(c_ulong(disconnect_id))

	conn.send(response, reliability=Reliability.Unreliable)
