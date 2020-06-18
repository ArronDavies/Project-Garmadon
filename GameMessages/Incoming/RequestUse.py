from uuid import uuid3, NAMESPACE_DNS

from Packets.Outgoing import *
from bitstream import *
from pyraknet.transports.abc import *


def RequestUse(stream, conn, server):
	bIsMultiInteractUse = stream.read(c_bit)
	multiInteractID = stream.read(c_ulong)
	multiInteractType = stream.read(c_long)
	object = stream.read(c_longlong)
	secondary = stream.read(c_bit)

	address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	uid = str(uuid3(NAMESPACE_DNS, str(address)))
	session = server.get_session(uid)

	for _ in server.objects:
		if server.objects[_].objid == object:
			try:
				use_cases[16](stream, conn, server, object)
			except KeyError:
				print("Unhandled RequestUse")

			break
		else:
			pass


def HandleVendorRequest(stream, conn, server, object):
	response = WriteStream()
	CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x0c, response=response)
	response.write(c_longlong(object))
	response.write(c_ushort(0x171))
	conn.send(response, reliability=Reliability.Reliable)

	response2 = WriteStream()
	CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x0c, response=response2)
	response2.write(c_longlong(object))
	response2.write(c_ushort(0x1a1))
	response2.write(c_bit(False))
	response2.write(c_ulong(1))
	response2.write(c_long(3038))
	response2.write(c_long(0))
	conn.send(response2, reliability=Reliability.Reliable)


use_cases = {}
use_cases[16] = HandleVendorRequest
