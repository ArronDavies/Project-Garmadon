from pyraknet.replicamanager import Replica
from bitstream import *
from Types.Vector3 import Vector3
from Types.Vector4 import Vector4


class ControllablePhysics(Replica):
	def __init__(self, controllable_physics_dict):
		self._is_jetpack_equipped = controllable_physics_dict['IsJetpackEquipped']
		self._jetpack_effect = controllable_physics_dict['JetpackEffect']
		self._is_jetpack_in_air = controllable_physics_dict['IsJetpackInAir']

		self._modify_movement = controllable_physics_dict['ModifyMovement']
		self._run_speed_multiplier = controllable_physics_dict['RunSpeedMultiplier']
		self._gravity_multiplier = controllable_physics_dict['GravityMultiplier']
		self._is_player = controllable_physics_dict['IsPlayer']
		self._player_pos = controllable_physics_dict['PlayerPos']
		self._player_rot = controllable_physics_dict['PlayerRot']
		self._is_on_ground = controllable_physics_dict['IsOnGround']
		self._is_on_rail = controllable_physics_dict['IsOnRail']
		self._is_velocity = controllable_physics_dict['IsVelocity']
		self._velocity = controllable_physics_dict['Velocity']
		self._is_angular_velocity = controllable_physics_dict['IsAngularVelocity']
		self._angular_velocity = controllable_physics_dict['AngularVelocity']
		self._is_on_platform = controllable_physics_dict['IsOnPlatform']

	def part1(self, stream):
		stream.write(c_bit(self._is_jetpack_equipped))
		if self._is_jetpack_equipped:
			stream.write(c_ulong(self._jetpack_effect))
			stream.write(c_bit(self._is_jetpack_in_air))  # Is jetpack in air
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
		stream.write(c_bit(self._modify_movement))
		if self._modify_movement:
			stream.write(c_float(self._gravity_multiplier))  # Grav multiplier
			stream.write(c_float(self._run_speed_multiplier))  # Speed multiplier

		flag = False
		stream.write(c_bit(flag))
		if flag:
			stream.write(c_ulong(1))  # Unknown
			stream.write(c_bit(True))  # Unknown

		flag2 = False
		stream.write(c_bit(flag2))
		if flag2:
			flag3 = False
			stream.write(c_bit(flag3))
			if flag3:
				stream.write(c_ulong(0))  # Unknown
				stream.write(c_bit(False))  # Unknown

		stream.write(c_bit(self._is_player))

		if self._is_player:
			stream.write(c_float(self._player_pos.x))
			stream.write(c_float(self._player_pos.y))
			stream.write(c_float(self._player_pos.z))

			stream.write(c_float(self._player_rot.x))
			stream.write(c_float(self._player_rot.y))
			stream.write(c_float(self._player_rot.z))
			stream.write(c_float(self._player_rot.w))

			stream.write(c_bit(self._is_on_ground))
			stream.write(c_bit(self._is_on_rail))

			stream.write(c_bit(self._is_velocity))

			if self._is_velocity:
				stream.write(c_float(self._velocity.x))
				stream.write(c_float(self._velocity.y))
				stream.write(c_float(self._velocity.z))

			stream.write(c_bit(self._is_angular_velocity))

			if self._is_angular_velocity:
				stream.write(c_float(self._angular_velocity.x))
				stream.write(c_float(self._angular_velocity.y))
				stream.write(c_float(self._angular_velocity.z))

			stream.write(c_bit(False))  # NOTE: Flag if on moving platform
			# TODO: Implement this flag even if it is not needed

		#stream.write(c_bit(self._is_player))

	def part3(self, stream):
		stream.write(c_bit(False))  # NOTE: Unknown should the be true?

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)
		self.part2(stream)

	def serialize(self, stream: WriteStream) -> None:
		self.part2(stream)
		self.part3(stream)

	def on_destruction(self) -> None:

		raise NotImplementedError