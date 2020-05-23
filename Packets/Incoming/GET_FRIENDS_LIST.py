from bitstream import *
from Packets.Outgoing import *

def GET_FRIENDS_LIST(stream, conn, server):
	unknown = stream.read(c_bit)
	GET_FRIENDS_LIST_RESPONSE.GET_FRIENDS_LIST_RESPONSE(stream, conn, server)