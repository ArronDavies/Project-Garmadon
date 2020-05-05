from pyraknet.transports.abc import *
import Packets.Outgoing
from bitstream import *


def GENERAL_NOTIFY(conn, notify_id):
	response = WriteStream()

	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x00, 0x01, response=response)

	response.write(c_ulong(notify_id))

	conn.send(response, reliability=Reliability.Reliable)
