from pyraknet.transports.abc import *
from Packets.Outgoing import *
from bitstream import *
from MasterAPI import *
import database


def CHARACTER_LIST_RESPONSE(stream, conn):
	session = get_session_from_connection(conn.get_address()[0], conn.get_address()[1])
	chardata = session['Character Data']

	accountdata = database.get_account_data_from_username(session['Username'])

	characters = database.get_character_data_from_accountid(accountdata["id"])

	response = WriteStream()

	CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x06, response=response)

	response.write(c_ubyte(len(characters)))  # Character Count
	response.write(c_ubyte(accountdata['FrontCharacter']))  # Front Character

	if len(characters) > 0:
		for character in characters:
			charid = character['CharID']

			response.write(c_longlong(character['ObjectID']))  # Character object ID
			set_character_data_value_from_connection(id=charid, valuetochange="Object ID", newvalue=character['ObjectID'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(0))  # ???

			response.write(character['Name'], allocated_length=33)  # Character object ID
			set_character_data_value_from_connection(id=charid, valuetochange="Name", newvalue=character['Name'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(character['UnapprovedName'], allocated_length=33)  # Minifigure Unapproved Name
			set_character_data_value_from_connection(id=charid, valuetochange="Unapproved Name", newvalue=character['UnapprovedName'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_bool(0))  # is name moderation rejected
			response.write(c_bool(0))  # is free to play
			response.write(str(""), allocated_length=5)  # unknown

			response.write(c_ulong(character['ShirtColor']))  # shirt color
			set_character_data_value_from_connection(id=charid, valuetochange="Shirt Color", newvalue=character['ShirtColor'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(character['ShirtStyle']))  # shirt style
			set_character_data_value_from_connection(id=charid, valuetochange="Shirt Style", newvalue=character['ShirtStyle'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(character['PantsColor']))  # pants color
			set_character_data_value_from_connection(id=charid, valuetochange="Pants Color", newvalue=character['PantsColor'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(character['HairStyle']))  # hair style
			set_character_data_value_from_connection(id=charid, valuetochange="Hair Style", newvalue=character['HairStyle'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(character['HairColor']))  # hair color
			set_character_data_value_from_connection(id=charid, valuetochange="Hair Color", newvalue=character['HairColor'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(character['LeftHand']))  # left hand
			set_character_data_value_from_connection(id=charid, valuetochange="Left Hand", newvalue=character['LeftHand'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(character['RightHand']))  # right hand
			set_character_data_value_from_connection(id=charid, valuetochange="Right Hand", newvalue=character['RightHand'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(character['Eyebrows']))  # eyebrows
			set_character_data_value_from_connection(id=charid, valuetochange="Eyebrows", newvalue=character['Eyebrows'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(character['Eyes']))  # eyes
			set_character_data_value_from_connection(id=charid, valuetochange="Eyes", newvalue=character['Eyes'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(character['Mouth']))  # mouth
			set_character_data_value_from_connection(id=charid, valuetochange="Mouth", newvalue=character['Mouth'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ulong(0))  # unknown 2

			response.write(c_ushort(character['LastZone']))  # last zone if 0 will do intro cinematic
			set_character_data_value_from_connection(id=charid, valuetochange="Last Zone", newvalue=character['LastZone'], ip=conn.get_address()[0], port=conn.get_address()[1])

			response.write(c_ushort(0))  # last instance
			response.write(c_ulong(0))  # last clone
			response.write(c_ulonglong(character['LastLog']))  # last logout time stamp
			response.write(c_ushort(0))  # number of items to follow

	conn.send(response, reliability=Reliability.Reliable)

