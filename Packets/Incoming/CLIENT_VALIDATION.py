import Packets.Outgoing
from bitstream import *
from MasterAPI import *


def CLIENT_VALIDATION(stream, conn):
	username = stream.read(str, allocated_length=33)
	user_key = stream.read(str, allocated_length=33)
	somehashedstring = stream.read(bytes, 32)
	unknown1 = stream.read(bytes, 1)
	session = get_session_from_connection(ip=conn.get_address()[0], port=conn.get_address()[1])

	if user_key == session['User Key']:
		if session['First Validate Done'] == False:
			set_session_data_value_from_connection("First Validate Done", True, conn.get_address()[0], conn.get_address()[1])
		elif session['First Validate Done'] == True:
			Packets.Outgoing.LOAD_STATIC_ZONE.LOAD_STATIC_ZONE(stream, conn)
