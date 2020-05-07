from pyraknet.transports.abc import *
import Packets.Outgoing
from bitstream import *
from MasterAPI import *
import os
import database
from Checksums import *


def LOAD_STATIC_ZONE(stream, conn):
	print("")
	response = WriteStream()
	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x02, response=response)

	session = get_session_from_connection(conn.get_address()[0], conn.get_address()[1])
	chardata = database.get_character_data_from_id(int(session['Current Character ID']))

	zone_name = ZONE_IDS(1000).name
	checksum = ZONE_CHECKSUMS[zone_name].value

	response.write(c_ushort(int(chardata['LastZone'])))
	response.write(c_ushort(0))
	response.write(c_ulong(0))
	response.write(c_ulong(checksum)) # checksum
	response.write(c_ushort(0))  # ???

	response.write(c_float(ZONE_SPAWNPOINTS[int(chardata['LastZone'])].x))  # x
	response.write(c_float(ZONE_SPAWNPOINTS[int(chardata['LastZone'])].y))  # y
	response.write(c_float(ZONE_SPAWNPOINTS[int(chardata['LastZone'])].z))  # z
	response.write(c_ulong(0))  # if activity world 4 else 0

	conn.send(response, reliability=Reliability.Reliable)