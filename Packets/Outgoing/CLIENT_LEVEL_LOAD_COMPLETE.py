from pyraknet.transports.abc import *
from GameMessages.ServerDoneLoadingAllObjects import ServerDoneLoadingAllObjects
from GameMessages.PlayerReady import PlayerReady
from Packets.Outgoing.CONSTRUCT_PACKET_HEADER import CONSTRUCT_PACKET_HEADER
from Replica.Player import Player
import zlib
from Enums import *


def CLIENT_LEVEL_LOAD_COMPLETE(stream, conn, master): # This is a massive mess TODO Make not a massive mess
    zoneid = stream.read(c_ushort)
    instance = stream.read(c_ushort)
    clone = stream.read(c_ulong)

    session = master.get_session(conn.get_address())
    accountdata = session.get_account_data()
    characterdata = session.get_current_character_data()

    zoneinstance = master.get_zone_instance(zoneid)

    replicamanager = zoneinstance.get_replica_manager()

    ldf = LegoData()

    # ldf.write('accountID', accountdata["id"], data_type=c_longlong)
    # ldf.write('chatmode', 0, data_type=c_long)
    # ldf.write('editor_enabled', False, data_type=c_bool)
    # ldf.write('editor_level', 0, data_type=c_long)
    # ldf.write('gmlevel', 0, data_type=c_long)

    # if zoneid == 0:
    # ldf.write('levelid', 1000, data_type=c_longlong)
    # else:
    # ldf.write('levelid', zoneid, data_type=c_longlong)

    ldf.write('name', characterdata['Name'], data_type=str, data_num=0)
    ldf.write('objid', characterdata['ObjectID'], data_type=c_longlong, data_num=9)
    # ldf.write('reputation', 100, data_type=c_longlong)
    ldf.write('template', 1, data_type=c_long)

    ldf_stream = WriteStream()
    ldf_stream.write(ldf)

    ldf_bytes = bytes(ldf_stream)
    compressed = zlib.compress(ldf_bytes)

    response = WriteStream()
    CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x04, response=response)
    response.write(c_ulong(len(compressed) + 9))  # size of following data
    response.write(c_bool(True))  # is content compressed
    response.write(c_ulong(len(ldf_bytes)))  # compressed data in LDF format, variable length
    response.write(c_ulong(len(compressed)))
    response.write(compressed)

    conn.send(response, reliability=Reliability.Reliable)

    replicamanager.add_participant(conn=conn)

    player = Player(char=characterdata, pos=ZONE_SPAWNPOINTS[characterdata["LastZone"]])
    replicamanager.construct(player, True)

    obj_load = ServerDoneLoadingAllObjects(objid=characterdata["ObjectID"], message_id=0x66a)
    conn.send(obj_load, reliability=Reliability.Reliable)

    player_ready = PlayerReady(objid=characterdata["ObjectID"], message_id=0x1fd)
    conn.send(player_ready, reliability=Reliability.Reliable)

# flag_change = NotifyClientFlagChange(objid=characterdata["ObjectID"], message_id=0x01d8, bFlag=False, iFlagID=0)
# conn.send(flag_change, reliability=Reliability.Reliable)
