from bitstream import *
from pyraknet.replicamanager import Replica


class PhantomPhysics(Replica):
	def __init__(self, phantom_physics_dict):
		self.phantom_physics_dict = phantom_physics_dict

	def part1(self, stream):
		if self.phantom_physics_dict['HasPosition']:
			stream.write(c_float(self.phantom_physics_dict['PosX']))
			stream.write(c_float(self.phantom_physics_dict['PosY']))
			stream.write(c_float(self.phantom_physics_dict['PosZ']))

			stream.write(c_float(self.phantom_physics_dict['RotX']))
			stream.write(c_float(self.phantom_physics_dict['RotY']))
			stream.write(c_float(self.phantom_physics_dict['RotZ']))
			stream.write(c_float(self.phantom_physics_dict['RotW']))

		stream.write(c_bit(False))  # TODO: Add toggle for this!!!

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		self.part1(stream)

	def on_destruction(self) -> None:
		raise NotImplementedError
