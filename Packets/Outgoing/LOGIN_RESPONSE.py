from uuid import uuid3, uuid4, NAMESPACE_DNS
from pyraknet.transports.abc import *
import Packets.Outgoing
from bitstream import *
import configparser
import bcrypt

config = configparser.ConfigParser()
config.read('config.ini')
char_server_details = config['CHARACTER']


def LOGIN_RESPONSE(stream, conn, server):
    address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
    uid = str(uuid3(NAMESPACE_DNS, str(address)))
    session = server.get_session(uid)
    session.sync_account_values_down()

    if session.username is not None:  # Username exists
        if bcrypt.checkpw(session.temp_password.encode('utf-8'),
                          session.password.encode('utf-8')):  # Password is correct
            if session.is_banned == 0:  # Not banned
                returncode = 0x01  # Success
                session.set_session_key(str(uuid4())[0:20])
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
    response.write(session.session_key, allocated_length=33)

    response.write(bytes(char_server_details['Host'], 'latin1'),
                   allocated_length=33)  # Char IP  TODO: Read this from a config file
    response.write(bytes('0.0.0.0', 'latin1'), allocated_length=33)  # Chat IP UNUSED
    response.write(c_ushort(int(char_server_details['Port'])))  # char Port
    response.write(c_ushort(0000))  # chat port UNUSED
    response.write(bytes("0", 'latin1'), allocated_length=33)  # Unknown data string maybe fallback server?
    response.write(bytes("00000000-0000-0000-0000-000000000000", 'latin1'),
                   allocated_length=37)  # Unknown, global unique id
    response.write(c_ulong(0))  # Unknown, always 0?
    response.write(bytes("US", 'latin1'), allocated_length=3)  # Localisation, currently only US and IT
    response.write(c_bool(session.first_login))  # First time logging in with subscription? Yes for us
    response.write(c_bool(False))  # Is FTP?
    response.write(c_ulonglong(0))  # Unknown data, always 0?

    response.write("Project Garmadon Error", length_type=c_ushort)  # Custom error message
    response.write(c_ushort(0))
    response.write(c_ulong(4))
    conn.send(response, reliability=Reliability.Reliable)
