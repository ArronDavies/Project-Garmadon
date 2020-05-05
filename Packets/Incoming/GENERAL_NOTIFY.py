import Packets.Outgoing
from bitstream import *


def DISCONNECT_NOTIFY(stream, conn):
	notify_id = stream.read(c_ulong)
