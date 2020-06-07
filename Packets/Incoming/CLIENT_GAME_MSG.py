from pyraknet.transports.abc import *
from bitstream import *
from Logger import *
from Packets.Outgoing import *
from GameMessages.Incoming import *

def CLIENT_GAME_MSG(stream, conn, server):
	lwoobjid = stream.read(c_longlong)
	message_id = stream.read(c_ushort)
	clean_message_id = format(message_id, '04x')

	messages = {}
	messages['0352'] = ParseChatMessage.ParseChatMessage
	messages['016c'] = RequestUse.RequestUse
	#messages['01d7'] = SetFlag.SetFlag
	#messages['007c'] = SelectSkill.SelectSkill
	#messages['00e9'] = UnEquipInventory.UnEquipInventory

	if clean_message_id == "0378":
		pass
	else:
		try:
			messages[clean_message_id](stream, conn, server)
			log(LOGGINGLEVEL.GAMEMESSAGE, " [" + str(server.zone_id) + "] Handled", str(clean_message_id))
		except KeyError:
			log(LOGGINGLEVEL.GAMEMESSAGE, " [" + str(server.zone_id) + "] Unhandled", str(clean_message_id))