from bitstream import *
from pyraknet.replicamanager import Replica


class Stats(Replica):
	def __init__(self, stats_dict):
		self._has_stats = stats_dict['HasStats']

		if self._has_stats:
			self._health = stats_dict['Health']
			self._max_health = stats_dict['MaxHealth']

			self._armor = stats_dict['Armor']
			self._max_armor = stats_dict['MaxArmor']

			self._imagination = stats_dict['Imagination']
			self._max_imagination = stats_dict['MaxImagination']

			self._damage_absorption_points = stats_dict['DamageAbsorptionPoints']
			self._is_immune = stats_dict['IsImmune']
			self._is_gm_immune = stats_dict['IsGMImmune']
			self._is_shielded = stats_dict['IsShielded']

			self._factions = stats_dict['Factions']

			self._is_smashable = stats_dict['IsSmashable']

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
		stream.write(c_bit(self._has_stats))

		if self._has_stats:
			stream.write(c_ulong(self._health))
			stream.write(c_float(self._max_health))  # Note: same as below but does nothing

			stream.write(c_ulong(self._armor))
			stream.write(c_float(self._max_armor))  # Note: same as below but does nothing

			stream.write(c_ulong(self._imagination))
			stream.write(c_float(self._max_imagination))  # Note: same as below but does nothing

			stream.write(c_ulong(0))  # NOTE: Damage absorption points
			stream.write(c_bit(True))  # NOTE: Immunity
			stream.write(c_bit(False))  # NOTE: GM immune
			stream.write(c_bit(False))  # NOTE: is shielded

			stream.write(c_float(self._max_health))
			stream.write(c_float(self._max_armor))
			stream.write(c_float(self._max_imagination))

			stream.write(c_ulong(len(self._factions)))

			for faction_id in self._factions:
				stream.write(c_long(faction_id))

			stream.write(c_bit(self._is_smashable))

	def part3(self, stream):
		if self._has_stats:
			stream.write(c_bit(False))  # NOTE: unknown(?)
			stream.write(c_bit(False))  # NOTE: same as above

			if self._is_smashable:
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
