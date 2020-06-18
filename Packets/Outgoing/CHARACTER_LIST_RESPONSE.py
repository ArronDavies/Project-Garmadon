from uuid import uuid3, NAMESPACE_DNS
from pyraknet.transports.abc import *
from Packets.Outgoing import *
from bitstream import *


def CHARACTER_LIST_RESPONSE(stream, conn, server):
	address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	uid = str(uuid3(NAMESPACE_DNS, str(address)))
	session = server.get_session(uid)
	session.sync_characters_down()

	response = WriteStream()

	CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x06, response=response)

	response.write(c_ubyte(len(session.characters)))  # Character Count
	response.write(c_ubyte(0))  # TODO: Implement front character

	if len(session.characters) > 0:
		for character in session.characters:
			response.write(c_longlong(character.object_id))  # Character object ID
			response.write(c_ulong(0))  # ???

			response.write(character.name, allocated_length=33)  # Character object ID
			response.write(character.unapproved_name, allocated_length=33)  # Minifigure Unapproved Name

			response.write(c_bool(0))  # is name moderation rejected
			response.write(c_bool(0))  # is free to play
			response.write(str(""), allocated_length=5)  # unknown

			response.write(c_ulong(character.shirt_color))  # shirt color
			response.write(c_ulong(character.shirt_style))  # shirt style

			response.write(c_ulong(character.pants_color))  # pants color

			response.write(c_ulong(character.hair_style))  # hair style
			response.write(c_ulong(character.hair_color))  # hair color

			response.write(c_ulong(character.left_hand))  # left hand
			response.write(c_ulong(character.right_hand))  # right hand

			response.write(c_ulong(character.eyebrows))  # eyebrows
			response.write(c_ulong(character.eyes))  # eyes
			response.write(c_ulong(character.mouth))  # mouth

			response.write(c_ulong(0))  # unknown 2

			response.write(c_ushort(character.last_zone))  # Note: If zero it will play into cinematic
			response.write(c_ushort(0))  # TODO: Implement Last Instance
			response.write(c_ulong(0))  # TODO: Implement Last Clone
			response.write(c_ulonglong(0))  # TODO: Implement Last Logout Timestamp

			character.sync_inventory_down()

			count = 0
			equipped_item_list = []
			for item in character.inventory:
				if item['IsEquipped'] == 1:
					equipped_item_list.append(item['ItemLOT'])
					count = count + 1

			response.write(c_ushort(count))  # number of items to follow#

			for item in equipped_item_list:
				response.write(c_ulong(int(item)))

	conn.send(response, reliability=Reliability.Reliable)
