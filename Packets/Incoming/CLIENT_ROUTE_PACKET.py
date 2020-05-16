from bitstream import *
from Logger import *


def CLIENT_ROUTE_PACKET(stream, conn, server):
	_packets = {}

	length_of_following = stream.read(c_ulong)
	rpid = 0x53
	rct = stream.read(c_ushort)
	pid = stream.read(c_ulong)
	padding = stream.read(c_ubyte)

	identifier = format(rpid, '02x') + "-" + format(rct, '02x') + "-" + format(padding, '02x') + "-" + format(pid, '02x')
	try:
		_packets[identifier](stream, conn, server)
		log(LOGGINGLEVEL.WORLDDEBUGROUTE, " [" + server.zone_id + "] Handled", identifier)
	except KeyError:
		log(LOGGINGLEVEL.WORLDDEBUGROUTE, " [" + server.zone_id + "] Unhandled", identifier)