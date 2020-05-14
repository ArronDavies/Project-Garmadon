from uuid import uuid3, uuid4, NAMESPACE_DNS
import Packets.Outgoing
from bitstream import *
import configparser
import uuid

config = configparser.ConfigParser()
config.read('config.ini')
char_info = config['CHARACTER']


def CLIENT_VALIDATION(stream, conn, server):
	username = stream.read(str, allocated_length=33)
	user_key = stream.read(str, allocated_length=33)
	somehashedstring = stream.read(bytes, 32)
	unknown1 = stream.read(bytes, 1)

	address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	uid = str(uuid3(NAMESPACE_DNS, str(address)))
	session = server.get_session(uid)
	session.temp_username = username
	session.sync_account_values_down()

	if user_key == session.session_key:
		if session.first_validate is True:
			pass
			# Packets.Outgoing.LOAD_STATIC_ZONE.LOAD_STATIC_ZONE(stream, conn)
	else:
		pass
		# TODO: Kick Player
