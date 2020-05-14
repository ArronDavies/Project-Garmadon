from bitstream import *
from pyraknet.replicamanager import Replica
from DataTypes import *


class Component107(Replica):
	def part1(self, stream):
		stream.write(c_bit(True))  # NOTE: unknown
		stream.write(c_longlong(0))

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		self.part1(stream)

	def on_destruction(self) -> None:
		raise NotImplementedError