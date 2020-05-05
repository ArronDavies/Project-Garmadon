from pyraknet.transports.abc import *
import Packets.Outgoing
from bitstream import *
from MasterAPI import *
import configparser
import database
import bcrypt
import uuid

config = configparser.ConfigParser()
config.read('../config.ini')
char_server_details = config['CHARACTER']
chat_server_details = config['CHAT']


def LOGIN_RESPONSE(stream, conn, username, password):

	accountdata = database.get_account_data_from_username(username)
	key = "0"
	if accountdata is not None:  # Username exists
		if bcrypt.checkpw((password).encode('utf-8'), (accountdata['Password']).encode('utf-8')):  # Password is correct
			if accountdata['IsBanned'] == 0:  # Not banned
				returncode = 0x01  # Success
				set_session_data_value_from_connection(valuetochange="Account ID", newvalue=accountdata['id'], ip=conn.get_address()[0], port=conn.get_address()[1])
				set_session_data_value_from_connection(valuetochange="Username", newvalue=str(username), ip=conn.get_address()[0], port=conn.get_address()[1])
				set_session_data_value_from_connection(valuetochange="Password", newvalue=str(accountdata['Password']), ip=conn.get_address()[0], port=conn.get_address()[1])
				key = (str(uuid.uuid4()))[0:20]
				set_session_data_value_from_connection(valuetochange="User Key", newvalue=str(key), ip=conn.get_address()[0], port=conn.get_address()[1])
			else:
				returncode = 0x02  # Account is banned
		else:
			returncode = 0x06  # Invalid Password
	else:
		returncode = 0x06  # Invalid Username

	response = WriteStream()
	Packets.Outgoing.CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x00, response=response)

	response.write(c_ubyte(returncode))
	response.write(bytes("Talk_Like_A_Pirate", 'latin1'), allocated_length=33)
	response.write(bytes("", 'latin1'), allocated_length=33 * 7)
	response.write(c_ushort(1))
	response.write(c_ushort(10))
	response.write(c_ushort(64))
	response.write(key, allocated_length=33)

	response.write(bytes(char_server_details['Host'], 'latin1'), allocated_length=33)  # Char IP  TODO: Read this from a config file
	response.write(bytes(chat_server_details['Host'], 'latin1'), allocated_length=33)  # Chat IP
	response.write(c_ushort(int(char_server_details['Port'])))  # char Port
	response.write(c_ushort(int(chat_server_details['Port'])))  # chat port
	response.write(bytes("0", 'latin1'), allocated_length=33)  # Unknown data string maybe fallback server?
	response.write(bytes("00000000-0000-0000-0000-000000000000", 'latin1'), allocated_length=37)  # Unknown, global unique id
	response.write(c_ulong(0))  # Unknown, always 0?
	response.write(bytes("US", 'latin1'), allocated_length=3)  # Localisation, currently only US and IT
	response.write(c_bool(accountdata['FirstLogin']))  # First time logging in with subscription? Yes for us
	response.write(c_bool(False))  # Is FTP?
	response.write(c_ulonglong(0))  # Unknown data, always 0?

	response.write("Pika-Chew :D", length_type=c_ushort)  # Custom error message
	response.write(c_ushort(0))
	response.write(c_ulong(4))
	conn.send(response, reliability=Reliability.Reliable)

