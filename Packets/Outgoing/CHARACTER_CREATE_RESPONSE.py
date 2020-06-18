from pyraknet.transports.abc import *
from bitstream import *
from Packets.Outgoing import CONSTRUCT_PACKET_HEADER


def CHARACTER_CREATE_RESPONSE(stream, conn, successful):
    response = WriteStream()
    CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x07, response=response)
    response.write(c_ubyte(successful))
    conn.send(response, reliability=Reliability.Reliable)
