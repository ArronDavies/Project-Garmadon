from bitstream import *
from database import *
from MasterAPI import *
import linecache
from Packets.Outgoing import *
import random

def CLIENT_CHARACTER_CREATE_REQUEST(stream, conn):

	minifigure_name = stream.read(str, allocated_length=33)  # wstring 66 bytes
	first_name = stream.read(c_ulong)
	second_name = stream.read(c_ulong)
	third_name = stream.read(c_ulong)
	unknown = stream.read(bytes, allocated_length=9)
	shirt_color = stream.read(c_ulong)
	shirt_style = stream.read(c_ulong)
	pants_color = stream.read(c_ulong)
	hair_style = stream.read(c_ulong)
	hair_color = stream.read(c_ulong)
	left_hand = stream.read(c_ulong)
	right_hand = stream.read(c_ulong)
	eyebrows = stream.read(c_ulong)
	eyes = stream.read(c_ulong)
	mouth = stream.read(c_ulong)
	unknown2 = stream.read(c_ubyte)

	objectid = random.randint(0, 99999999999)

	firstname = linecache.getline('clientfiles/minifigname_first.txt', first_name + 1)
	middlename = linecache.getline('clientfiles/minifigname_middle.txt', second_name + 1)
	lastname = linecache.getline('clientfiles/minifigname_last.txt', third_name + 1)
	unaprovedname = firstname.rstrip() + middlename.rstrip() + lastname.rstrip()

	doesnameexist = check_if_minifig_name_exists(minifigure_name)
	session = get_session_from_connection(conn.get_address()[0], conn.get_address()[1])

	if doesnameexist is None:  # No character with name exists
		create_character(session['Account ID'], objectid, minifigure_name, unaprovedname, shirt_color, shirt_style, pants_color, hair_style, hair_color, left_hand, right_hand, eyebrows, eyes, mouth)

		chardata = get_character_data_from_objid(objectid)
		set_session_data_value_from_connection(valuetochange="Current Character ID", newvalue=chardata['CharID'], ip=conn.get_address()[0], port=conn.get_address()[1])
		CHARACTER_CREATE_RESPONSE.CHARACTER_CREATE_RESPONSE(stream, conn, 0x00)  # Succesfull
		CHARACTER_LIST_RESPONSE.CHARACTER_LIST_RESPONSE(stream, conn)

	else:
		CHARACTER_CREATE_RESPONSE.CHARACTER_CREATE_RESPONSE(stream, conn, 0x04)