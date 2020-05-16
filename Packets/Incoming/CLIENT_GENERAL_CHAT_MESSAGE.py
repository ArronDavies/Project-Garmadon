from bitstream import *
from Packets.Outgoing import *
from uuid import uuid3, uuid4, NAMESPACE_DNS

def CLIENT_GENERAL_CHAT_MESSAGE(stream, conn, server):
	address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	uid = str(uuid3(NAMESPACE_DNS, str(address)))
	sendersession = server.get_session(uid)

	byte1 = stream.read(c_ubyte)
	byte2 = stream.read(c_ubyte)
	byte3 = stream.read(c_ubyte)

	length = stream.read(c_ulong)

	message = stream.read(str, allocated_length=length)

	commands = {}
	commands['!tp'] = server.transfer_world
	commands['!wear_item'] = server.wear_item
	commands['!fly'] = server.fly

	args = message.split(' ')  # Note: arg[0] is the command312

	if args[0].startswith('!'):
		if args[0] == "!help":
			GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, str("!tp <zone>"), "", 0)
			GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, str("!wear_item <lot>"), "", 0)
			GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, str("!fly"), "", 0)
		else:
			try:
				commands[args[0]](sendersession, args)
			except KeyError:
				GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, str("That command does not exist"), "", 0)
	else:
		for session in server._sessions:
			Packets.Outgoing.GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, server._sessions[session].connection, server, message=message, sender_name=sendersession.current_character.name, sender_objid=sendersession.current_character.object_id)