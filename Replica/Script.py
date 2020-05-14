from bitstream import *
from pyraknet.replicamanager import Replica
from DataTypes import *


class Script(Replica):
	def __init__(self, script=False):
		self.script = script

	def part1(self, stream):
		stream.write(c_bit(self.script))

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		raise NotImplementedError

	def on_destruction(self) -> None:
		raise NotImplementedError