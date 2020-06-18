from bitstream import *


def UnEquipInventory(stream, conn, server):
	bEvenIfDead = stream.read(c_bit)
	bIgnoreCooldown = stream.read(c_bit)
	bOutSuccess = stream.read(c_bit)
	itemtounequip = stream.read(c_longlong)
	replacementObjectID = stream.read(c_longlong)
	print(bEvenIfDead)
	print(bIgnoreCooldown)
	print(bOutSuccess)
	print(itemtounequip)
	print(replacementObjectID)
