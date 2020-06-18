from bitstream import *
from Packets.Outgoing import CONSTRUCT_PACKET_HEADER


def NotifyClientFlagChange(objid, message_id, bFlag, iFlagID):
    response = WriteStream()
    CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x0c, response=response)
    response.write(c_longlong(objid))
    response.write(c_ushort(message_id))
    response.write(c_bool(bFlag))
    response.write(c_long(iFlagID))

    return response
