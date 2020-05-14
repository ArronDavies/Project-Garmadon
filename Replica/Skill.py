from bitstream import *
from pyraknet.replicamanager import Replica
from DataTypes import *


class Skill(Replica):
	def part1(self, stream):
		stream.write(c_bool(False))  # TODO: add a var for this

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		pass

	def on_destruction(self) -> None:
		raise NotImplementedError