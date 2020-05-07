from bitstream import *
import database
from Packets.Outgoing import *
from MasterAPI import *


def CLIENT_CHARACTER_RENAME_REQUEST(stream, conn):
	objectID = stream.read(c_longlong)
	new_name = stream.read(str, allocated_length=33)

	doesnameexist = database.check_if_minifig_name_exists(new_name)

	if doesnameexist is None:  # No character with name exists
		database.set_character_name_from_objectid(id=objectID, name=new_name)

		character = database.get_character_data_from_objid(objectID)
		set_character_data_value_from_connection(id=character['CharID'], valuetochange='Name', newvalue=new_name, ip=conn.get_address()[0], port=conn.get_address()[1])
		CHARACTER_RENAME_RESPONSE.CHARACTER_RENAME_RESPONSE(stream, conn, 0x00)
	else:
		CHARACTER_RENAME_RESPONSE.CHARACTER_RENAME_RESPONSE(stream, conn, 0x03)