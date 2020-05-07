from bitstream import *
import database
from Packets.Outgoing import *
from MasterAPI import *


def CLIENT_LOGIN_REQUEST(stream, conn):
	objectID = stream.read(c_longlong)

	chardata = database.get_character_data_from_objid(objectID)
	set_session_data_value_from_connection(valuetochange="Current Character ID", newvalue=chardata['CharID'], ip=conn.get_address()[0], port=conn.get_address()[1])

	TRANSFER_TO_WORLD.TRANSFER_TO_WORLD(stream, conn, 0, objectID)