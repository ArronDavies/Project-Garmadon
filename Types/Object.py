from Packets.Replica import *


class Object(BaseData.BaseData):
	def __init__(self, object_id, name, lot, spawner_object_id=None):
		super().__init__(objid=object_id, lot=lot, spawner=spawner_object_id, name=name)
		self.components = []