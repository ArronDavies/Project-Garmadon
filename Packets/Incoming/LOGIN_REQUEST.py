import Packets.Outgoing
from bitstream import *


def LOGIN_REQUEST(stream, conn):
	username = stream.read(str, allocated_length=33)
	password = stream.read(str, allocated_length=41)

	comlang = stream.read(c_ushort)
	unknown = stream.read(c_ubyte)
	process_memory_client = stream.read(str, allocated_length=256)
	gpu_driver_info = stream.read(str, allocated_length=128)
	dwNumberOfProcessors = stream.read(c_ulong)
	dwProcessorType = stream.read(c_ulong)
	dwProcessorLevel = stream.read(c_ushort)
	dwProcessorRevision = stream.read(c_ushort)
	unknown2 = stream.read(c_ulong)
	dwMajorVersion = stream.read(c_ulong)
	dwMinorVersion = stream.read(c_ulong)
	dwBuildNumber = stream.read(c_ulong)
	dwPlatformId = stream.read(c_ulong)

	Packets.Outgoing.LOGIN_RESPONSE.LOGIN_RESPONSE(stream, conn, username, password)
