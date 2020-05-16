from bitstream import *
from Packets.Outgoing import *
from uuid import uuid3, uuid4, NAMESPACE_DNS
from Logger import *


def ParseChatMessage(stream, conn, server):
	pass
	# address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
	# uid = str(uuid3(NAMESPACE_DNS, str(address)))
	# session = server.get_session(uid)
	#
	# pass
	#
	# commands = {}
	# commands['/tp'] = server.transfer_world
	# commands['/wear_item'] = server.wear_item
	# commands['/fly'] = server.fly
	#
	# iClientState = stream.read(c_int)
	# message = stream.read(bytes, allocated_length=33)
	#
	# args = message.split(' ')  # Note: arg[0] is the command
	#
	# if args[0].startswith('/'):
	# 	if args[0] == "/help":
	# 		GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, bytes("/tp <zone>"), 0, 0)
	# 		GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, bytes("/wear_item <lot>"), 0, 0)
	# 		GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, bytes("/fly"), 0, 0)
	# 	else:
	# 		try:
	# 			if args[1] is None:
	# 				args[1] = 1
	# 			commands[args[0]](session, args[1])
	# 		except KeyError:
	# 			GENERAL_CHAT_MESSAGE.GENERAL_CHAT_MESSAGE(stream, conn, server, bytes("That command does not exist or was typed incorrectly"), 0, 0)