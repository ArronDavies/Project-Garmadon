from bitstream import *
from Logger import *
from Packets.Incoming import *


# This handel's re routed packet such as ones for mail and friends.

def CLIENT_ROUTE_PACKET(stream, conn, server):
    packets = {}
    packets['53-02-00-0a'] = Packets.Incoming.GET_FRIENDS_LIST.GET_FRIENDS_LIST

    length_of_following = stream.read(c_ulong)
    rpid = 0x53
    rct = stream.read(c_ushort)
    pid = stream.read(c_ulong)
    padding = stream.read(c_ubyte)
    identifier = format(rpid, '02x') + "-" + format(rct, '02x') + "-" + format(padding, '02x') + "-" + format(pid,
                                                                                                              '02x')
    try:
        packets[identifier](stream, conn, server)
        log(LOGGINGLEVEL.WORLDDEBUGROUTE, " [" + server.zone_id + "] Handled", identifier)
    except KeyError:
        log(LOGGINGLEVEL.WORLDDEBUGROUTE, " [" + server.zone_id + "] Unhandled", identifier)
