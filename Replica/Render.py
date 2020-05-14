from bitstream import *
from pyraknet.replicamanager import Replica
from DataTypes import *


class Render(Replica):
	def part1(self, stream):
		activeeffects = 0

		stream.write(c_ulong(activeeffects))

		i = 0
		while i < activeeffects:
			effectname = "name"
			print(effectname)
			stream.write(c_ubyte(len(effectname)))

			l = 0
			while l < len(effectname):
				stream.write(c_ubyte(effectname[l]))
				l += 1

			i += 1

			stream.write(c_ulong(0))  # Effect ID

	# TODO: Complete this component

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		pass

	def on_destruction(self) -> None:
		raise NotImplementedError