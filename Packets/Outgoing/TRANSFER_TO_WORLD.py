from uuid import uuid3, uuid4, NAMESPACE_DNS
from pyraknet.transports.abc import *
from Packets.Outgoing import *
from bitstream import *
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def TRANSFER_TO_WORLD(stream, conn, server, is_transfer=False, zone_id=0):
	if is_transfer:
		address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
		uid = str(uuid3(NAMESPACE_DNS, str(address)))
		session = server.get_session(uid)

		world_server_details = config[str(zone_id)]
		response = WriteStream()
		Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x0e, response=response)
		response.write(bytes(world_server_details['Host'], 'latin1'), allocated_length=33)  # Note: IP of world server
		response.write(c_ushort(int(world_server_details['Port'])))  # Note: Port of world server
		response.write(c_bool(1))  # Note: If true will say dimension shift success
		conn.send(response, reliability=Reliability.Unreliable)
	else:
		objectid = stream.read(c_longlong)

		address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
		uid = str(uuid3(NAMESPACE_DNS, str(address)))
		session = server.get_session(uid)

		for character in session.characters:
			if character.object_id == objectid:
				session.set_current_character_id(charid=character.id)
				session.current_character = character
				break

		if session.current_character.last_zone == 0:
			world_server_details = config['1000']
		else:
			world_server_details = config[str(session.current_character.last_zone)]

		response = WriteStream()
		Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x0e, response=response)
		response.write(bytes(world_server_details['Host'], 'latin1'), allocated_length=33)  # Note: IP of world server
		response.write(c_ushort(int(world_server_details['Port'])))  # Note: Port of world server
		response.write(c_bool(0))  # Note: If true will say dimension shift success
		conn.send(response, reliability=Reliability.Reliable)
