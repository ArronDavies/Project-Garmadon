from bitstream import *
from pyraknet.replicamanager import Replica


class Render(Replica):
	def __init__(self, render_dict):
		self._effects = render_dict # Just like this or error because we set no effects

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

	# 	stream.write(c_ulong(len(self._effects)))
	# 	for effect in self._effects:
	# 		stream.write(c_ubyte(len(effect['name'])))
	#
	# 		for char in effect['name']:
	# 			stream.write(c_ubyte(char))
	#
	# 		stream.write(c_ulong(effect['id']))

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		pass

	def on_destruction(self) -> None:
		raise NotImplementedError
