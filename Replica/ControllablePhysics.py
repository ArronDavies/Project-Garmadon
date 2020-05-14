from bitstream import *
from pyraknet.replicamanager import Replica
from DataTypes import *


class ControllablePhysics(Replica):
	def __init__(self, jetpack=False, jetpack_effect=0, player=True, player_pos=Vector3(0, 0, 0), player_rot=Vector4(0, 0, 0, 0), player_ground=True, player_rail=False, player_velocity=False, player_velocity_vec=Vector3(0, 0, 0), player_angular_velocity=False, player_angular_velocity_vec=Vector3(0, 0, 0), player_platform=False):
		self.jetpack = jetpack
		self.jetpack_effect = jetpack_effect
		self.player = player
		self.player_pos = player_pos
		self.player_rot = player_rot
		self.player_ground = player_ground
		self.player_rail = player_rail
		self.player_velocity = player_velocity
		self.player_velocity_vec = player_velocity_vec
		self.player_angular_velocity = player_angular_velocity
		self.player_angular_velocity_vec = player_angular_velocity_vec
		self.player_platform = player_platform

	# Creation Only
	def part1(self, stream):
		stream.write(c_bit(self.jetpack))
		if self.jetpack:
			stream.write(c_ulong(self.jetpack_effect))
			stream.write(c_bit(False))  # Is jetpack in air
			stream.write(c_bit(False))  # Unknown

		flag = True  # Unknown flag
		stream.write(c_bit(flag))
		if flag:
			stream.write(c_ulong(0))  # Unknown 1
			stream.write(c_ulong(0))  # Unknown 2
			stream.write(c_ulong(0))  # Unknown 3
			stream.write(c_ulong(0))  # Unknown 4
			stream.write(c_ulong(0))  # Unknown 5
			stream.write(c_ulong(0))  # Unknown 6
			stream.write(c_ulong(0))  # Unknown 7

	def part2(self, stream):
		movementmodifier = False
		stream.write(c_bit(movementmodifier))
		if movementmodifier:
			stream.write(c_float(1))  # Grav multiplier
			stream.write(c_float(1))  # Speed multiplier

		flag = False
		stream.write(c_bit(flag))
		if flag:
			stream.write(c_ulong(1))  # Unknown
			stream.write(c_bit(1))  # Unknown

		flag2 = False
		stream.write(c_bit(flag2))
		if flag2:
			flag3 = False
			stream.write(c_bit(flag3))
			if flag3:
				stream.write(c_ulong(0))  # Unknown
				stream.write(c_bit(0))  # Unknown

		stream.write(c_bit(self.player))

		if self.player:
			stream.write(c_float(self.player_pos.x))
			stream.write(c_float(self.player_pos.y))
			stream.write(c_float(self.player_pos.z))

			stream.write(c_float(self.player_rot.x))
			stream.write(c_float(self.player_rot.y))
			stream.write(c_float(self.player_rot.z))
			stream.write(c_float(self.player_rot.w))

			stream.write(c_bit(self.player_ground))
			stream.write(c_bit(self.player_rail))

			stream.write(c_bit(self.player_velocity))

			if self.player_velocity:
				stream.write(c_float(self.player_velocity_vec.x))
				stream.write(c_float(self.player_velocity_vec.y))
				stream.write(c_float(self.player_velocity_vec.z))

			stream.write(c_bit(self.player_angular_velocity))

			if self.player_angular_velocity:
				stream.write(c_float(self.player_angular_velocity_vec.x))
				stream.write(c_float(self.player_angular_velocity_vec.y))
				stream.write(c_float(self.player_angular_velocity_vec.z))

			stream.write(c_bit(False))  # NOTE: unknown flag
			# TODO: Implement this flag even if it is unknown

	def part3(self, stream):
		stream.write(c_bit(False))  # NOTE: should this be true?

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)
		self.part2(stream)

	def serialize(self, stream: WriteStream) -> None:
		self.part2(stream)
		self.part3(stream)

	def on_destruction(self) -> None:

		raise NotImplementedError
