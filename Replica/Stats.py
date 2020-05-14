from bitstream import *
from pyraknet.replicamanager import Replica



class Stats(Replica):
	def __init__(self, stats=True, health=4, max_health=4, armor=0, max_armor=4, imagination=6, max_imagination=6, factions=[0], smashable=False):
		self.stats = stats
		self.health = health
		self.max_health = max_health
		self.armor = armor
		self.max_armor = max_armor
		self.imagination = imagination
		self.max_imagination = max_imagination
		self.factions = factions
		self.smashable = smashable

	def part1(self, stream):
		flag = True

		stream.write(c_bit(flag))
		if flag:
			stream.write(c_ulong(0))  # Unknown 1
			stream.write(c_ulong(0))  # Unknown 2
			stream.write(c_ulong(0))  # Unknown 3
			stream.write(c_ulong(0))  # Unknown 4
			stream.write(c_ulong(0))  # Unknown 5
			stream.write(c_ulong(0))  # Unknown 6
			stream.write(c_ulong(0))  # Unknown 7
			stream.write(c_ulong(0))  # Unknown 8
			stream.write(c_ulong(0))  # Unknown 9

	def part2(self, stream):
		stream.write(c_bit(self.stats))

		if self.stats:
			stream.write(c_ulong(self.health))
			stream.write(c_float(self.max_health))

			stream.write(c_ulong(self.armor))
			stream.write(c_float(self.max_armor))

			stream.write(c_ulong(self.imagination))
			stream.write(c_float(self.max_imagination))

			stream.write(c_ulong(0))  # NOTE: unknown
			stream.write(c_bit(True))
			stream.write(c_bit(False))
			stream.write(c_bit(False))

			stream.write(c_float(self.max_health))
			stream.write(c_float(self.max_armor))
			stream.write(c_float(self.max_imagination))

			stream.write(c_ulong(len(self.factions)))

			for faction_id in self.factions:
				stream.write(c_long(faction_id))

			stream.write(c_bit(self.smashable))

	def part3(self, stream):
		if self.stats:
			stream.write(c_bit(False))  # NOTE: unknown(?)
			stream.write(c_bit(False))  # NOTE: same as above

			if self.smashable:
				stream.write(c_bit(False))  # NOTE: unknown
				stream.write(c_bit(False))  # NOTE: same as above
				# If this ^ then u32 unknown

	def part4(self, stream):
		flag = True

		stream.write(c_bit(flag))
		if flag:
			stream.write(c_bit(False))

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)
		self.part2(stream)
		self.part3(stream)
		self.part4(stream)

	def serialize(self, stream: WriteStream) -> None:
		self.part2(stream)
		self.part4(stream)

	def on_destruction(self) -> None:
		raise NotImplementedError