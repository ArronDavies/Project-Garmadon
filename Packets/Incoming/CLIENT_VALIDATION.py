import Packets.Outgoing
from bitstream import *
import uuid
from MasterAPI import *

config = configparser.ConfigParser()
config.read('../config.ini')
char_info = config['CHARACTER']


def CLIENT_VALIDATION(stream, conn):
	username = stream.read(str, allocated_length=33)
	user_key = stream.read(str, allocated_length=33)
	somehashedstring = stream.read(bytes, 32)
	unknown1 = stream.read(bytes, 1)
	session = get_session_from_connection(ip=conn.get_address()[0], port=conn.get_address()[1])

	if user_key == session['User Key']:
		if str(session['First Validate Done']) == "False":
			set_session_data_value_from_connection("First Validate Done", True, conn.get_address()[0], conn.get_address()[1])
		elif str(session['First Validate Done']) == "True":
			Packets.Outgoing.LOAD_STATIC_ZONE.LOAD_STATIC_ZONE(stream, conn)
	else:
		address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		kick_player(char_info['Host'], char_info['Port'], uid)
