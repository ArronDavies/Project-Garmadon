from pyraknet.transports.abc import *
import Packets.Outgoing
from bitstream import *
from MasterAPI import *
import database
import json
import uuid


def TRANSFER_TO_WORLD(stream, conn, isShift, objectID):
	response = WriteStream()

	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x0e, response=response)

	chardata = database.get_character_data_from_objid(objectID)
	character_zone = str(chardata['LastZone'])

	zone = get_zone(character_zone)
	zone = json.loads(zone)

	if zone:
		for instance in zone:
			if zone[instance]['Players'] < 32:
				set_zone_instance_value(character_zone, instance, 'Players', zone[instance]['Players'] + 1)

				address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
				uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
				add_session_to_instance(zone_id=str(chardata['LastZone']), session_uuid=uid, instance_uuid=instance)

				response.write(bytes(zone[instance]['IP'], 'latin1'), allocated_length=33)
				response.write(c_ushort(int(zone[instance]['Port'])))
				response.write(c_bool(isShift))
				break

	conn.send(response, reliability=Reliability.Reliable)

	# if zone in zones:
	# 	zone = get_zone(character_zone)
	# 	print(zone)
	# 	dict = json.loads(zone)
	# 	print(dict)
	# 	for instance in dict:
	# 		print(instance[1])
	# 	if len(zones['1100'].keys()) > 0:
	# 		for instance in zones['1100']:
	# 			if instance['Players'] < 32:
	# 				set_zone_instance_value(character_zone, instance, 'Players', instance['Players'] + 1)
	# 				break
	# 	else:
	# 		pass
	# 		# Make new zone
	# else:
	# 	pass
	# 	# Make new one
	# 	ip = requests.get('https://api.ipify.org').text
	# 	create_zone_instance(zone_id=character_zone, ip=ip,)
	#
