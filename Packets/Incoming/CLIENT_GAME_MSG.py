from pyraknet.transports.abc import *
from bitstream import *
from Logger import *
from Packets.Outgoing import *
import struct

def CLIENT_GAME_MSG(stream, conn, server):
	lwoobjid = stream.read(c_longlong)
	message_id = stream.read(c_ushort)
	clean_message_id = format(message_id, '04x')

	log(LOGGINGLEVEL.GAMEMESSAGE, " [" + str(server.zone_id) + "] Unhandled", str(clean_message_id))
