from bitstream import *
import database
from Packets.Outgoing import *
from MasterAPI import *


def CLIENT_CHARACTER_DELETE_REQUEST(stream, conn):
	objectID = stream.read(c_longlong)
	print(int(objectID))

	chardata = database.get_character_data_from_objid(objectID)
	cid = chardata['CharID']

	database.delete_character_from_objectid(objectID)
	delete_character_from_connection(cid, conn.get_address()[0], conn.get_address()[1])

	DELETE_CHARACTER_RESPONSE.DELETE_CHARACTER_RESPONSE(stream, conn, 0x01)