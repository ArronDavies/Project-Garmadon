from pyraknet.transports.abc import Reliability

from Packets.Replica import *
import sqlite3
from Utils.GetProjectRoot import get_project_root
import random
from Logger import LOGGINGLEVEL, log

non_networked = [12, 31, 35, 36, 45, 55, 56, 64, 65, 68, 73, 104, 113, 114]
network_components = [108, 61, 1, 3, 20, 30, 40, 7, 23, 26, 4, 17, 5, 9, 60, 48, 25, 49, 16, 6, 39, 71, 75, 42, 2, 107,
					  69]
available_components = [3, 40, 7, 17, 9, 16, 2, 107]


class Object(BaseData.BaseData):
	def __init__(self, object_id, name, lot, spawner_object_id=None):
		super().__init__(objid=object_id, lot=lot, name=name)

		self.position_x = None
		self.position_y = None
		self.position_z = None

		self.rotation_x = None
		self.rotation_y = None
		self.rotation_z = None
		self.rotation_w = None

		self.spawner = None  # If this is not None then it should be handled by the spawner

		self.settings = {}

		self.component_ids = []
		self.components = []

		self.is_constructable = True

	def start(self, server):
		self.server = server
		if self.settings['loadOnClientOnly'].split(':')[1] == "1":
			pass
		else:
			self.create()

	def get_components(self):
		db = sqlite3.connect(str(str(get_project_root()) + "/clientfiles/cdclient.sqlite"))
		dbcmd = db.cursor()

		query = "SELECT component_type, component_id FROM ComponentsRegistry WHERE id = ?"
		dbcmd.execute(query, (self.lot,))
		object_components = dbcmd.fetchall()

		for component in network_components:
			for _ in object_components:
				if component == _[0]:
					if component not in non_networked:
						self.component_ids.append(_)

		for component in self.component_ids:
			if component[0] in available_components:
				pass
			else:
				self.is_constructable = False
				break

	def create(self):
		for component in self.component_ids:
			if component[0] == 3:
				simple_physics_dict = {'HasPosition': True, 'PosX': self.position_x, 'PosY': self.position_y,
									   'PosZ': self.position_z, 'RotX': self.rotation_x, 'RotY': self.rotation_y,
									   'RotZ': self.rotation_z, 'RotW': self.rotation_w}
				simple_physics_dict['HasVelocity'] = False
				simple_physics_dict['LVelocityX'] = 0
				simple_physics_dict['LVelocityY'] = 0
				simple_physics_dict['LVelocityZ'] = 0

				simple_physics_dict['AVelocityX'] = 0
				simple_physics_dict['AVelocityY'] = 0
				simple_physics_dict['AVelocityZ'] = 0

				self.components.append(SimplePhysics.SimplePhysics(simple_physics_dict=simple_physics_dict))

			if component[0] == 40:
				phantom_physics_dict = {'HasPosition': True, 'PosX': self.position_x, 'PosY': self.position_y,
										'PosZ': self.position_z, 'RotX': self.rotation_x, 'RotY': self.rotation_y,
										'RotZ': self.rotation_z, 'RotW': self.rotation_w}
				self.components.append(PhantomPhysics.PhantomPhysics(phantom_physics_dict=phantom_physics_dict))

			if component[0] == 7:
				destructible_dict = {}
				stats_dict = {}
				stats_dict['HasStats'] = False

				self.components.append(Destructible.Destructible(destructible_dict=destructible_dict))
				self.components.append(Stats.Stats(stats_dict=stats_dict))

			if component[0] == 17:
				inventory_dict = {}

				db = sqlite3.connect(str(str(get_project_root()) + "/clientfiles/cdclient.sqlite"))
				dbcmd = db.cursor()
				query = "SELECT itemid, count, equip FROM InventoryComponent WHERE id = ?"
				dbcmd.execute(query, (component[1],))
				items = dbcmd.fetchall()

				inventory = []

				for item in items:
					itm = {}
					itm['ItemID'] = random.randrange(0, 10000000)
					itm['ItemLOT'] = item[0]
					itm['Quantity'] = item[1]
					itm['IsEquipped'] = item[2]
					itm['Slot'] = items.index(item)

					db = sqlite3.connect(str(str(get_project_root()) + "/clientfiles/cdclient.sqlite"))
					dbcmd = db.cursor()
					query = "SELECT itemType FROM ItemComponent WHERE id = ?"
					dbcmd.execute(query, (itm['ItemLOT'],))
					item_type = dbcmd.fetchall()

					try:
						itm['Type'] = item_type[0][0]
					except Exception:
						itm['Type'] = 0

					inventory.append(itm)

				inventory_dict['HasInventory'] = True
				inventory_dict['Inventory'] = inventory

				self.components.append(Inventory.Inventory(inventory_dict=inventory_dict))

			if component[0] == 5:
				db = sqlite3.connect(str(str(get_project_root()) + "/clientfiles/cdclient.sqlite"))
				dbcmd = db.cursor()
				query = "SELECT client_script_name FROM ScriptComponent WHERE id = ?"
				dbcmd.execute(query, (component[1],))
				script = dbcmd.fetchone()

				try:
					if script[0] is not None:
						self.is_constructable = False
						pass
					else:
						pass  # log(LOGGINGLEVEL.ERROR, "LOT: " + self.spawn_lot + " Has No Script")
				except Exception:
					self.is_constructable = False
					log(LOGGINGLEVEL.ERROR, "LOT: " + str(self.lot) + " No script database entry")

				if self.is_constructable is True:
					script_dict = {}
					self.components.append(Script.Script(script_dict=script_dict))

			if component[0] == 9:
				skill_dict = {}

				self.components.append(Skill.Skill(skill_dict=skill_dict))

			if component[0] == 16:
				vendor_dict = {}

				self.components.append(Vendor.Vendor(vendor_dict=vendor_dict))

			if component[0] == 2:
				render_dict = {}

				self.components.append(Render.Render(render_dict=render_dict))

			if component[0] == 107:
				component107_dict = {}
				self.components.append(Component107.Component107(component107_dict=component107_dict))

		self.server._rep_man.construct(obj=self, new=True, reliability=Reliability.ReliableOrdered)
