from bitstream import *
from pyraknet.replicamanager import Replica


class Skill(Replica):
    def __init__(self, skill_dict):
        self._skill_dict = skill_dict

    def part1(self, stream):
        stream.write(c_bool(False))  # TODO: add a var for this

    def write_construction(self, stream: WriteStream) -> None:
        self.part1(stream)

    def serialize(self, stream: WriteStream) -> None:
        pass

    def on_destruction(self) -> None:
        raise NotImplementedError
