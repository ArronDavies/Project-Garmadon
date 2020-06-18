from bitstream import *
from pyraknet.replicamanager import Replica


class Vendor(Replica):
    def __init__(self, vendor_dict):
        self.vendor_dict = vendor_dict

    def part1(self, stream):
        flag = False
        stream.write(c_bit(flag))

        if flag:
            stream.write(c_bit(False))
            stream.write(c_bit(False))

    def write_construction(self, stream: WriteStream) -> None:
        self.part1(stream)

    def serialize(self, stream: WriteStream) -> None:
        self.part1(stream)

    def on_destruction(self) -> None:
        raise NotImplementedError
