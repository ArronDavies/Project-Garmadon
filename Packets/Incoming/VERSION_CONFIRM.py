import Packets.Outgoing
from bitstream import *


def VERSION_CONFIRM(stream, conn):
	game_version = stream.read(c_ulong)
	unknown = stream.read(c_ulong)
	remote_connection_type = stream.read(c_ulong)
	process_id = stream.read(c_ulong)
	local_port = stream.read(c_ushort)
	local_ip = stream.read(bytes, allocated_length=33)  # Unused on client

	Packets.Outgoing.VERSION_CONFIRM.VERSION_CONFIRM(stream, conn)
