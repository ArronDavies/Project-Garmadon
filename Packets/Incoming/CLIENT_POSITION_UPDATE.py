from uuid import uuid3, NAMESPACE_DNS
from Types.Vector3 import Vector3
from Types.Vector4 import Vector4
from bitstream import *
import time


# This packet updates characters place in the DB and other clients

def CLIENT_POSITION_UPDATE(stream, conn, server):
    address = (str(conn.get_address()[0]), int(conn.get_address()[1]))
    uid = str(uuid3(NAMESPACE_DNS, str(address)))
    session = server.get_session(uid)

    position = Vector3(stream.read(c_float), stream.read(c_float), stream.read(c_float))
    rotation = Vector4(stream.read(c_float), stream.read(c_float), stream.read(c_float), stream.read(c_float))

    session.current_character.player_object.components[0]._player_pos = position
    session.current_character.player_object.components[0]._player_rot = rotation
    session.current_character.player_object.components[0]._is_on_ground = stream.read(c_bit)
    session.current_character.player_object.components[0]._is_on_rail = stream.read(c_bit)

    is_velocity = stream.read(c_bit)
    session.current_character.player_object.components[0]._is_velocity = is_velocity
    if is_velocity:
        velocity = Vector3(stream.read(c_float), stream.read(c_float), stream.read(c_float))
        session.current_character.player_object.components[0]._velocity = velocity

    is_angular_velocity = stream.read(c_bit)
    session.current_character.player_object.components[0]._is_angular_velocity = is_angular_velocity
    if is_angular_velocity:
        angular_velocity = Vector3(stream.read(c_float), stream.read(c_float), stream.read(c_float))
        session.current_character.player_object.components[0]._angular_velocity = angular_velocity

    is_on_platform = stream.read(c_bit)
    if is_on_platform:
        pass
    # TODO: Implement is on platform

    replica_manager = server.get_rep_man()

    replica_manager.serialize(session.current_character.player_object)
