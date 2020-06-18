from bitstream import *


def CONSTRUCT_PACKET_HEADER(rpid, rct, ipid, response):
	response.write(c_ubyte(rpid))
	response.write(c_ushort(rct))
	response.write(c_ulong(ipid))
	response.write(c_ubyte(0))  # Padded byte?
