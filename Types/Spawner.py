import threading
import sqlite3
from Types.Item import Item
from Types.Inventory import Inventory as typeinv
from Types.Object import Object
from Types.LWOOBJID import LWOOBJID
from Utils.GetProjectRoot import get_project_root
import time
from Packets.Replica import *
from multiprocessing import Process
import random


non_networked = [12, 31, 35, 36, 45, 55, 56, 64, 65, 68, 73, 104, 113, 114]
network_components = [108, 61, 1, 3, 20, 30, 40, 7, 23, 26, 4, 17, 5, 9, 60, 48, 25, 49, 16, 6, 39, 71, 75, 42, 2, 107, 69]

available_components = [3, 40, 7, 17, 9, 16, 2, 107]


class Spawner:
	def __init__(self):
		self.spawner_object_id = None

		self.spawn_lot = None

		self.pos_x = None
		self.pos_y = None
		self.pos_z = None

		self.rot_x = None
		self.rot_y = None
		self.rot_z = None
		self.rot_w = None

		self.scale = None

		self.settings = {}

		self.components = []

		self.max_to_spawn = None
		self.respawn = None
		self.is_spawned = False
		self.no_timed_spawn = None
		self.load_on_client_only = None

		self.is_smashable = False
		self.is_constructable = True

		self.server = None
		self.process = None

	def start(self, server):
		self.server = server
		if self.load_on_client_only == "1":
			pass
		else:
			self.create()
			# self.spawner_object_id = LWOOBJID().generatespawner()
			# spawner = Object(object_id=self.spawner_object_id, lot=176, name="")
			# self.server._rep_man.construct(spawner, True)

	# def keep_alive(self):
	# 	time_since_despawned = 100
	# 	if self.no_timed_spawn == "1":
	# 		if self.is_spawned:
	# 			pass
	# 		else:
	# 			self.is_spawned = True
	# 			self.create()
	# 	else:
	# 		if self.is_spawned:
	# 			pass
	# 		else:
	# 			if time_since_despawned >= int(self.respawn):
	# 				self.create()
	# 				self.is_spawned = True
	# 				time_since_despawned = 0
	# 			else:
	# 				time_since_despawned += 1

	def create(self):
		id = LWOOBJID().generateobject()
		obj = Object(object_id=id, lot=int(self.spawn_lot), name="")

		for component in self.components:
			if component[0] == 3:
				simple_physics_dict = {'HasPosition': True, 'PosX': self.pos_x, 'PosY': self.pos_y, 'PosZ': self.pos_z, 'RotX': self.rot_x, 'RotY': self.rot_y, 'RotZ': self.rot_z, 'RotW': self.rot_w}
				simple_physics_dict['HasVelocity'] = False
				simple_physics_dict['LVelocityX'] = 0
				simple_physics_dict['LVelocityY'] = 0
				simple_physics_dict['LVelocityZ'] = 0

				simple_physics_dict['AVelocityX'] = 0
				simple_physics_dict['AVelocityY'] = 0
				simple_physics_dict['AVelocityZ'] = 0

				obj.components.append(SimplePhysics.SimplePhysics(simple_physics_dict=simple_physics_dict))

			if component[0] == 40:
				phantom_physics_dict = {'HasPosition': True, 'PosX': self.pos_x, 'PosY': self.pos_y, 'PosZ': self.pos_z, 'RotX': self.rot_x, 'RotY': self.rot_y, 'RotZ': self.rot_z, 'RotW': self.rot_w}
				obj.components.append(PhantomPhysics.PhantomPhysics(phantom_physics_dict=phantom_physics_dict))

			if component[0] == 7:
				destructible_dict = {}
				stats_dict = {}
				stats_dict['HasStats'] = False

				obj.components.append(Destructible.Destructible(destructible_dict=destructible_dict))
				obj.components.append(Stats.Stats(stats_dict=stats_dict))

			if component[0] == 17:
				inventory_dict = {}

				db = sqlite3.connect(str(str(get_project_root()) + "/clientfiles/cdclient.sqlite"))
				dbcmd = db.cursor()
				query = "SELECT itemid, count, equip FROM InventoryComponent WHERE id = ?"
				dbcmd.execute(query, (component[1],))
				items = dbcmd.fetchall()

				inventory = typeinv(character=None)

				for item in items:
					itm = Item()
					itm.item_id = random.randrange(0, 10000000)
					itm.item_lot = item[0]
					itm.quantity = item[1]
					itm.is_equipped = item[2]
					itm.slot = items.index(item)
					itm.type = 0
					inventory.items.append(itm)

				inventory_dict['HasInventory'] = True
				inventory_dict['Inventory'] = inventory

				obj.components.append(Inventory.Inventory(inventory_dict=inventory_dict))
				print(self.spawn_lot)

			if component[0] == 9:
				skill_dict = {}

				obj.components.append(Skill.Skill(skill_dict=skill_dict))

			if component[0] == 16:
				vendor_dict = {}

				obj.components.append(Vendor.Vendor(vendor_dict=vendor_dict))

			if component[0] == 2:
				render_dict = {}

				obj.components.append(Render.Render(render_dict=render_dict))

			if component[0] == 107:
				component107_dict = {}
				obj.components.append(Component107.Component107(component107_dict=component107_dict))

		self.server._rep_man.construct(obj, True)



	def get_components(self):
		db = sqlite3.connect(str(str(get_project_root()) + "/clientfiles/cdclient.sqlite"))
		dbcmd = db.cursor()

		query = "SELECT component_type, component_id FROM ComponentsRegistry WHERE id = ?"
		dbcmd.execute(query, (self.spawn_lot,))
		object_components = dbcmd.fetchall()

		for component in network_components:
			for _ in object_components:
				if component == _[0]:
					if component not in non_networked:
						self.components.append(_)

		for component in self.components:
			if component[0] in available_components:
				pass
			else:
				self.is_constructable = False
				break

	def parse_settings(self):
		try:
			self.max_to_spawn = self.settings['max_to_spawn'].split(':')[1]
			self.no_timed_spawn = self.settings['no_timed_spawn'].split(':')[1]
			self.respawn = self.settings['respawn'].split(':')[1]
			self.load_on_client_only = self.settings['loadOnClientOnly'].split(':')[1]
			self.is_smashable = self.settings['is_smashable'].split(':')[1]
		except Exception:
			self.is_constructable = False
