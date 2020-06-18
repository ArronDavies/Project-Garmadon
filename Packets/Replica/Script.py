from bitstream import *
from pyraknet.replicamanager import Replica


class Script(Replica):
	def __init__(self, script_dict):
		self.script_dict = script_dict

	def part1(self, stream):
		stream.write(c_bit(False))

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		pass

	def on_destruction(self) -> None:
		raise NotImplementedError
