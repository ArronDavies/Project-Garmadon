from bitstream import *
from pyraknet.replicamanager import Replica


class Inventory(Replica):
    def __init__(self, inventory_dict):
        self._has_inventory = inventory_dict['HasInventory']
        self._inventory = inventory_dict['Inventory']

    def part1(self, stream):
        stream.write(c_bit(self._has_inventory))

        if self._has_inventory:
            count = 0
            for item in self._inventory:
                if item['IsEquipped']:
                    count = count + 1

            stream.write(c_ulong(count))  # Note: Number of items Equipped

            for item in self._inventory:
                if item['IsEquipped']:
                    stream.write(c_longlong(item['ItemID']))
                    stream.write(c_long(item['ItemLOT']))
                    stream.write(c_bit(False))
                    stream.write(c_bit(True))
                    stream.write(c_ulong(item['Quantity']))
                    stream.write(c_bit(True))
                    stream.write(c_ushort(item['Slot']))
                    stream.write(c_bit(True))
                    stream.write(c_ulong(item['Type']))
                    stream.write(c_bit(False))
                    stream.write(c_bit(True))

        stream.write(c_bit(False))

    def write_construction(self, stream: WriteStream) -> None:
        self.part1(stream)

    def serialize(self, stream: WriteStream) -> None:
        self.part1(stream)

    def on_destruction(self) -> None:
        raise NotImplementedError
