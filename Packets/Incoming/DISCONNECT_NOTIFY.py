import Packets.Outgoing
from bitstream import *


def DISCONNECT_NOTIFY(stream, conn):
	disconnect_id = stream.read(c_ulong)
