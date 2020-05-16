from Utils.GetProjectRoot import get_project_root
from Types.Item import Item
import sqlite3


class Inventory:
	def __init__(self, character):
		self.character = character
		self.items = []
		self.vault_items = []
		self.bricks = []
		self.temporary_items = []
		self.models = []
		self.temporary_models = []
		self.behaviours = []
		self.property_deeds = []
		self.hidden = []
		self.vault_models = []

	def add_item(self, item_data):
		self.sync_inventory_down()
		if item_data['Type'] == 0:
			if len(self.items) > 0:
				for item in self.items:
					if int(item.item_lot) == int(item_data['ItemLOT']):
						print("Same")
						item.quantity = item.quantity + item_data['Quantity']

						db = sqlite3.connect(str(str(get_project_root()) + "/PikaChewniverse.sqlite"))
						db.row_factory = sqlite3.Row
						dbcmd = db.cursor()
						query = "UPDATE Inventory SET Quantity = ? WHERE ItemID = ?"
						dbcmd.execute(query, (item.quantity, item.item_id,))
						db.commit()
						dbcmd.close()
						break

					elif len(self.items) < self.character.inventory_space:
						newitem = Item()
						newitem.item_lot = item_data['ItemLOT']
						newitem.quantity = item_data['Quantity']
						newitem.is_equipped = item_data['IsEquipped']
						newitem.is_linked = item_data['IsLinked']
						newitem.slot = len(self.items) + 1
						newitem.item_id = item_data['ItemID']
						newitem.type = item_data['Type']
						self.items.append(newitem)

						db = sqlite3.connect(str(str(get_project_root()) + "/PikaChewniverse.sqlite"))
						db.row_factory = sqlite3.Row
						dbcmd = db.cursor()
						query = "INSERT INTO Inventory (CharID, ItemLOT, IsEquipped, IsLinked, Quantity, Slot, ItemID, Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
						dbcmd.execute(query, (self.character.id, newitem.item_lot, newitem.is_equipped, newitem.is_linked, newitem.quantity, newitem.slot, newitem.item_id, newitem.type,))
						db.commit()
						dbcmd.close()
						break
			else:
				newitem = Item()
				newitem.item_lot = item_data['ItemLOT']
				newitem.quantity = item_data['Quantity']
				newitem.is_equipped = item_data['IsEquipped']
				newitem.is_linked = item_data['IsLinked']
				newitem.slot = len(self.items) + 1
				newitem.item_id = item_data['ItemID']
				newitem.type = item_data['Type']
				self.items.append(newitem)

				db = sqlite3.connect(str(str(get_project_root()) + "/PikaChewniverse.sqlite"))
				db.row_factory = sqlite3.Row
				dbcmd = db.cursor()
				query = "INSERT INTO Inventory (CharID, ItemLOT, IsEquipped, IsLinked, Quantity, Slot, ItemID, Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
				dbcmd.execute(query, (self.character.id, newitem.item_lot, newitem.is_equipped, newitem.is_linked, newitem.quantity, newitem.slot, newitem.item_id, newitem.type,))
				db.commit()
				dbcmd.close()

				del newitem
		else:
			print("Type not supported: " + str(item_data['Type']))
		self.sync_inventory_down()

	def sync_inventory_down(self):
		db = sqlite3.connect(str(str(get_project_root()) + "/PikaChewniverse.sqlite"))
		db.row_factory = sqlite3.Row
		dbcmd = db.cursor()
		query = "SELECT * FROM Inventory WHERE CharID = ?"
		dbcmd.execute(query, (self.character.id,))
		value = dbcmd.fetchall()
		self.items.clear()
		for item in value:
			newitem = Item()
			newitem.item_lot = item['ItemLOT']
			newitem.quantity = item['Quantity']
			newitem.is_equipped = item['IsEquipped']
			newitem.is_linked = item['IsLinked']
			newitem.slot = len(self.items) + 1
			newitem.item_id = item['ItemID']
			newitem.type = item['Type']
			self.items.append(newitem)

		dbcmd.close()

