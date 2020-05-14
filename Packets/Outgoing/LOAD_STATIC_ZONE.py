from Packets.Outgoing.CONSTRUCT_PACKET_HEADER import CONSTRUCT_PACKET_HEADER
from pyraknet.transports.abc import *
from Enums import *


def LOAD_STATIC_ZONE(stream, conn, master):
	session = master.get_session(connection=conn.get_address())
	characterdata = session.get_current_character_data()

	if characterdata['LastZone'] == 0:
		zone_name = ZONE_IDS(1000).name
		zone = 1000
	else:
		zone_name = ZONE_IDS(characterdata['LastZone']).name
		zone = characterdata['LastZone']

	checksum = ZONE_CHECKSUMS[zone_name].value

	response = WriteStream()
	CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x02, response=response)
	response.write(c_ushort(zone))  # zoneid
	response.write(c_ushort(0))  # map instance
	response.write(c_ulong(0))  # map clone
	response.write(c_ulong(checksum))  # map checksum
	response.write(c_ushort(0))  # ???
	response.write(c_float(ZONE_SPAWNPOINTS[zone].x))  # x
	response.write(c_float(ZONE_SPAWNPOINTS[zone].y))  # y
	response.write(c_float(ZONE_SPAWNPOINTS[zone].z))  # z
	response.write(c_ulong(0))  # if activity world 4 else 0

	conn.send(response, reliability=Reliability.Reliable)