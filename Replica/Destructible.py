from bitstream import *
from pyraknet.replicamanager import Replica
from DataTypes import *


class Destructible(Replica):
	def part1(self, stream):
		stream.write(c_bit(False))  # NOTE: unknown flag(?)
		stream.write(c_bit(False))  # NOTE: unknown flag

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		pass

	def on_destruction(self) -> None:
		raise NotImplementedError