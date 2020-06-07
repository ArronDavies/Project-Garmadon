from Utils.GetProjectRoot import get_project_root
from configparser import ConfigParser
from bitstream import *
from Types.Object import Object
from Types.LWOOBJID import LWOOBJID

# Note: Some of LCDRs code is used here namely reading the LVL files, big thanks to him!!!


class Scene:
	def __init__(self):
		self.luz_version = None
		self.zone_id = None
		self.file_name = None
		self.scene_id = None
		self.layer_id = None
		self.scene_name = None

		self.chunk_type = None
		self.chunk_length = None

		self.objects = []

	def get_objects(self):
		config = ConfigParser()
		config.read(str(get_project_root()) + "/config.ini")
		path = str(get_project_root()) + config[self.zone_id]['LVL']

		with open(path + self.file_name , "rb") as lvl:
			data = lvl.read()
			luz_len = len(data)
			stream = ReadStream(data, unlocked=True)

		header = stream.read(bytes, length=4)

		stream.read_offset = 0
		if header == b"CHNK":
			while not stream.all_read():
				assert stream.read_offset // 8 % 16 == 0  # seems everything is aligned like this?
				start_pos = stream.read_offset // 8
				stream.read(bytes, length=4) # b"CHNK"

				self.chunk_type = stream.read(c_uint)

				stream.read(c_ushort)
				stream.read(c_ushort)

				self.chunk_length = stream.read(c_uint)

				data_pos = stream.read(c_uint)
				stream.read_offset = data_pos * 8

				assert stream.read_offset // 8 % 16 == 0

				if self.chunk_type == 1000:
					pass
				elif self.chunk_type == 2000:
					pass
				elif self.chunk_type == 2001:
					self.parse_2001(stream)
				elif self.chunk_type == 2002:
					pass
				stream.read_offset = (start_pos + self.chunk_length) * 8  # go to the next CHNK
		else:
			self.parse_old_lvl(stream)
			self.parse_2001(stream)

	def parse_2001(self, stream):
		for object in range(stream.read(c_ulong)):
			object_id = stream.read(c_ulonglong)
			lot = stream.read(c_long)

			if self.luz_version >= 0x26:
				stream.read(c_ulong)  # Note: Asset type?

			if self.luz_version >= 0x20:
				stream.read(c_ulong)  # Note: Unknown

			pos_x = stream.read(c_float)
			pos_y = stream.read(c_float)
			pos_z = stream.read(c_float)
			rot_w = stream.read(c_float)
			rot_x = stream.read(c_float)
			rot_y = stream.read(c_float)
			rot_z = stream.read(c_float)
			scale = stream.read(c_float)

			settings = stream.read(str, length_type=c_uint)

			settings_dict = {}
			for setting in settings.split(u'\n'):
				x, y = setting.split('=')
				settings_dict[x] = y

			if lot == 176:

				obj_class = Object(lot=int(settings_dict['spawntemplate'].split(":")[1]), name="", object_id=LWOOBJID().generateobject())

				obj_class.position_x = pos_x
				obj_class.position_y = pos_y
				obj_class.position_z = pos_z
				obj_class.rotation_x = rot_x
				obj_class.rotation_y = rot_y
				obj_class.rotation_z = rot_z
				obj_class.rotation_w = rot_w
				obj_class.scale = scale

				obj_class.settings = settings_dict

				self.objects.append(obj_class)


			if self.luz_version >= 0x07:
				for _ in range(stream.read(c_ulong)):
					stream.read(bytes, length=64)
					stream.read(c_ulong)
					stream.read(c_bool)
					stream.read(bytes, length=16)
					stream.read(bytes, length=16)
					stream.read(bytes, length=16)
					stream.read(bytes, length=16)


	def parse_old_lvl(self, stream):
		version = stream.read(c_ushort)
		stream.read(c_ushort)
		stream.read(c_ubyte)
		stream.read(c_uint)
		if version >= 45:
			stream.read(c_float)
		for _ in range(4 * 3):
			stream.read(c_float)
		if version >= 31:
			if version >= 39:
				for _ in range(12):
					stream.read(c_float)
				if version >= 40:
					for _ in range(stream.read(c_uint)):
						stream.read(c_uint)
						stream.read(c_float)
						stream.read(c_float)
			else:
				stream.read(c_float)
				stream.read(c_float)

			for _ in range(3):
				stream.read(c_float)

		if version >= 36:
			for _ in range(3):
				stream.read(c_float)

		if version < 42:
			for _ in range(3):
				stream.read(c_float)
			if version >= 33:
				for _ in range(4):
					stream.read(c_float)

		stream.read(bytes, length_type=c_uint)
		for _ in range(5):
			stream.read(bytes, length_type=c_uint)
		stream.skip_read(4)
		for _ in range(stream.read(c_uint)):
			stream.read(c_float), stream.read(c_float), stream.read(c_float)

