from bitstream import *
from Packets.Outgoing import *
from uuid import uuid3, uuid4, NAMESPACE_DNS
import better_profanity


# Redirect packet for the chat server and moderation

def CLIENT_GENERAL_CHAT_MESSAGE(stream, conn, server):
	address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	uid = str(uuid3(NAMESPACE_DNS, str(address)))
	sendersession = server.get_session(uid)

	byte1 = stream.read(c_ubyte)
	byte2 = stream.read(c_ubyte)
	byte3 = stream.read(c_ubyte)

	length = stream.read(c_ulong)

	message = stream.read(bytes, length=length * 2)

	commands = {}
	commands['!tp'] = server.transfer_world
	commands['!fly'] = server.fly
	args = message.decode('utf-16le').rstrip(' \t\r\n\0').split(' ')  # Note: arg[0] is the command

	if args[0].startswith('!'):
		if args[0] == "!help":
			GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, str("!tp <zone>"), "", 0)
			GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, str("!fly"), "", 0)
		else:
			try:
				commands[args[0]](sendersession, args)
			except KeyError:
				GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, str("That command does not exist"), "",
														  0)
	else:
		if better_profanity.profanity.contains_profanity(str(message, 'latin1')):
			pass
		else:
			for session in server._sessions:
				Packets.Outgoing.GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, server._sessions[session].connection,
																		   server, message=message,
																		   sender_name=sendersession.current_character.name,
																		   sender_objid=sendersession.current_character.object_id)
