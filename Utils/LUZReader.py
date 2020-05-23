from bitstream import *
from configparser import ConfigParser
from Utils.GetProjectRoot import get_project_root
from Types.Zone import Zone
from Types.Scene import Scene


class LUZReader:
	def __init__(self, zone_id):
		self._zone_id = zone_id

		config = ConfigParser()
		config.read(str(get_project_root()) + "/config.ini")
		self.path = str(get_project_root()) + config[self._zone_id]['LUZ']

		self.version = None
		self.version_control = None
		self.world_id = None

		self.zone = Zone()

	def parse(self):
		with open(self.path, "rb") as file:
			data = file.read()
			luz_len = len(data)
			stream = ReadStream(data, unlocked=True)

		self.version = stream.read(c_ulong)

		if self.version >= 0x24:
			self.version_control = stream.read(c_ulong)

		self.world_id = stream.read(c_ulong)

		if self.version >= 0x26:
			self.zone.spawnpoint_pos_x = stream.read(c_float)
			self.zone.spawnpoint_pos_y = stream.read(c_float)
			self.zone.spawnpoint_pos_z = stream.read(c_float)

			self.zone.spawnpoint_rot_x = stream.read(c_float)
			self.zone.spawnpoint_rot_y = stream.read(c_float)
			self.zone.spawnpoint_rot_z = stream.read(c_float)
			self.zone.spawnpoint_rot_w = stream.read(c_float)

		if self.version < 0x25:
			scene_count = stream.read(c_ubyte)
		else:
			scene_count = stream.read(c_ulong)

		for _ in range(scene_count):
			scene = Scene()
			scene.luz_version = self.version
			scene.zone_id = self._zone_id
			scene.file_name = stream.read(bytes, length=stream.read(c_ubyte)).decode("latin1")
			scene.scene_id = stream.read(c_ulong)
			scene.layer_id = stream.read(c_ulong)
			scene.scene_name = stream.read(bytes, length=stream.read(c_ubyte)).decode("latin1")
			stream.read(bytes, length=3)
			self.zone.scenes.append(scene)