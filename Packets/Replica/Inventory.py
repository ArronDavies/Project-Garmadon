from bitstream import *
from pyraknet.replicamanager import Replica


class Inventory(Replica):
	def __init__(self, inventory_dict):
		self._has_inventory = inventory_dict['HasInventory']
		self._inventory = inventory_dict['Inventory']

	def part1(self, stream):
		stream.write(c_bit(self._has_inventory))

		if self._has_inventory:
			items = []
			count = 0
			for item in self._inventory.items:
				if item.is_equipped:
					count = count + 1
					items.append(item)

			stream.write(c_ulong(count))  # Note: Number of items Equipped

			for item in items:
				if item.is_equipped:
					stream.write(c_longlong(item.item_id))
					stream.write(c_long(item.item_lot))
					stream.write(c_bit(False))
					stream.write(c_bit(True))
					stream.write(c_ulong(item.quantity))
					stream.write(c_bit(True))
					stream.write(c_ushort(item.slot))
					stream.write(c_bit(True))
					stream.write(c_ulong(item.type))
					stream.write(c_bit(False))
					stream.write(c_bit(True))

		stream.write(c_bit(False))


	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)

	def serialize(self, stream: WriteStream) -> None:
		self.part1(stream)

	def on_destruction(self) -> None:
		raise NotImplementedError