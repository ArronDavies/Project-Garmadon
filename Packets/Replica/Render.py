from bitstream import *
from pyraknet.replicamanager import Replica
import sqlite3
from Utils.GetProjectRoot import get_project_root


class Render(Replica):
	def __init__(self, render_dict):
		self._effects = render_dict

	def part1(self, stream):
		stream.write(c_ulong(0))

	# new_list = []
	#
	# for effect in self._effects[0]:
	# 	if effect is not None:
	# 		new_list.append(effect)
	#
	# stream.write(c_ulong(len(new_list)))
	# for effect in new_list:
	# 	db = sqlite3.connect(str(str(get_project_root()) + "/clientfiles/cdclient.sqlite"))
	# 	dbcmd = db.cursor()
	# 	query = "SELECT effectName FROM BehaviorEffect WHERE effectID = ?"
	# 	dbcmd.execute(query, (effect,))
	# 	name = dbcmd.fetchone()
	#
	# 	if name is None or name[0] is None:
	# 		stream.write(c_ubyte(0))
	# 	else:
	# 		stream.write(c_ubyte(len(name[0])))
	# 		for char in name[0]:
	# 			stream.write(bytes(char, 'latin1'))
	#
	# 	stream.write(c_ulong(effect))
	#
	# 	query = "SELECT effectType FROM BehaviorEffect WHERE effectID = ?"
	# 	dbcmd.execute(query, (effect,))
	# 	type = dbcmd.fetchone()
	#
	# 	if type is None:
	# 		stream.write(c_ubyte(0))
	# 	else:
	# 		stream.write(c_ubyte(len(type[0])))
	# 		for char in type[0]:
	# 			stream.write(bytes(char, 'latin1'))
	#
	# 	stream.write(c_float(0))
	# 	stream.write(c_longlong(0))

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		pass

	def on_destruction(self) -> None:
		raise NotImplementedError
