from bitstream import *
from pyraknet.replicamanager import Replica


class SimplePhysics(Replica):
    def __init__(self, simple_physics_dict):
        self.simple_physics_dict = simple_physics_dict

    def part1(self, stream):
        stream.write(c_bit(False))  # Note: Unknown
        stream.write(c_long(0))  # Note: Unknown TODO: Explore as this might be scale?

    def part2(self, stream):
        has_velocity = self.simple_physics_dict['HasVelocity']
        stream.write(c_bit(has_velocity))
        if has_velocity:
            stream.write(c_float(self.simple_physics_dict['LVelocityX']))
            stream.write(c_float(self.simple_physics_dict['LVelocityY']))
            stream.write(c_float(self.simple_physics_dict['LVelocityZ']))

            stream.write(c_float(self.simple_physics_dict['AVelocityX']))
            stream.write(c_float(self.simple_physics_dict['AVelocityY']))
            stream.write(c_float(self.simple_physics_dict['AVelocityZ']))

        flag2 = False
        stream.write(c_bit(flag2))
        if flag2:
            stream.write(c_ulong(0))  # Note: Unknown

        has_position = self.simple_physics_dict['HasPosition']
        stream.write(c_bit(has_position))
        if has_position:
            stream.write(c_float(self.simple_physics_dict['PosX']))
            stream.write(c_float(self.simple_physics_dict['PosY']))
            stream.write(c_float(self.simple_physics_dict['PosZ']))
            stream.write(c_float(self.simple_physics_dict['RotX']))
            stream.write(c_float(self.simple_physics_dict['RotY']))
            stream.write(c_float(self.simple_physics_dict['RotZ']))
            stream.write(c_float(self.simple_physics_dict['RotW']))

    def write_construction(self, stream: WriteStream) -> None:
        self.part1(stream)
        self.part2(stream)

    def serialize(self, stream: WriteStream) -> None:
        self.part2(stream)

    def on_destruction(self) -> None:
        raise NotImplementedError
