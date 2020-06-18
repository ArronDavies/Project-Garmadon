from bitstream import *
import os
import zlib


def test():
	for file in os.listdir("../Utils/Packets"):
		with open("../Utils/Packets/" + file, 'rb') as f:
			content = f.read()
			stream = ReadStream(content)
			packet_header = stream.read(c_ubyte)

			# if packet_header == 0x24:
			# 	print("-------------------------------------------------------------------------")
			# 	print(file)
			# 	print("Packet Header ", hex(packet_header))
			# 	stream.read(c_bit)
			# 	print("Network ID ", stream.read(c_ushort))
			# 	print("Object ID ", stream.read(c_longlong))
			# 	lot = stream.read(c_long)
			# 	print("LOT ", lot)
			#
			# 	length = stream.read(c_ubyte)
			# 	print("Name ", stream.read(bytes, length=length * 2).decode('utf-16le').rstrip(' \t\r\n\0'))
			# 	print("Time Since Created ", stream.read(c_ulong))
			#
			# 	flag = stream.read(c_bit)
			# 	if flag:
			# 		size = stream.read(c_ulong)
			# 		stream.read(bytes, length=size)
			# 	# TODO: Implement this
			#
			# 	flag = stream.read(c_bit)
			#
			# 	flag = stream.read(c_bit)
			# 	if flag:
			# 		print("Spawner Object ID ", stream.read(c_longlong))
			#
			# 	flag = stream.read(c_bit)
			# 	if flag:
			# 		print("Spawner node ID ", stream.read(c_ulong))
			#
			# 	flag = stream.read(c_bit)
			# 	if flag:
			# 		print("Object Scale ", stream.read(c_float))
			#
			# 	flag = stream.read(c_bit)
			# 	if flag:
			# 		print("Object world state ", stream.read(c_ubyte))
			#
			# 	flag = stream.read(c_bit)
			# 	if flag:
			# 		print("GM Level ", stream.read(c_ubyte))
			#
			# 	flag = stream.read(c_bit)
			# 	if flag:
			# 		flag = stream.read(c_bit)
			# 		if flag:
			# 			print("Parent Object ID ", stream.read(c_longlong))
			# 			stream.read(c_bit)
			# 		flag = stream.read(c_bit)
			# 		if flag:
			# 			children_count = stream.read(c_ubyte)
			# 			count = 0
			# 			while count < children_count:
			# 				print("Child Object ", count, " ID ", stream.read(c_longlong))
			#
			# 	if lot == 1:
			# 		flag = stream.read(c_bit)
			# 		print("Is jetpack equipped ", flag)
			# 		if flag:
			# 			print("Jetpack effect ID ", stream.read(c_ulong))
			#
			# 		flag = stream.read(c_bit)
			# 		if flag:
			# 			stream.read(c_ulong)
			# 			stream.read(c_ulong)
			# 			stream.read(c_ulong)
			# 			stream.read(c_ulong)
			# 			stream.read(c_ulong)
			# 			stream.read(c_ulong)
			# 			stream.read(c_ulong)
			#
			# 		flag = stream.read(c_bit)
			# 		if flag:
			# 			stream.read(c_float)
			# 			stream.read(c_float)
			#
			# 		flag = stream.read(c_bit)
			# 		if flag:
			# 			stream.read(c_ulong)
			# 			stream.read(c_bit)
			#
			# 		flag = stream.read(c_bit)
			# 		if flag:
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stream.read(c_ulong)
			# 				stream.read(c_bit)
			#
			# 		flag = stream.read(c_bit)
			# 		if flag:
			# 			print("X position ", stream.read(c_float))
			# 			print("Y position ", stream.read(c_float))
			# 			print("Z position ", stream.read(c_float))
			# 			print("X rotation ", stream.read(c_float))
			# 			print("Y rotation ", stream.read(c_float))
			# 			print("Z rotation ", stream.read(c_float))
			# 			print("W rotation ", stream.read(c_float))
			# 			print("Is on ground ", stream.read(c_bit))
			# 			stream.read(c_bit)
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stream.read(c_float)
			# 				stream.read(c_float)
			# 				stream.read(c_float)
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stream.read(c_float)
			# 				stream.read(c_float)
			# 				stream.read(c_float)
			# 				stream.read(c_float)
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				print("Platform object ID ", stream.read(c_longlong))
			# 				stream.read(c_float)
			# 				stream.read(c_float)
			# 				stream.read(c_float)
			# 				flag = stream.read(c_bit)
			# 				if flag:
			# 					stream.read(c_float)
			# 					stream.read(c_float)
			# 					stream.read(c_float)
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stuct_count = stream.read(c_ulong)
			# 				count = 0
			# 				while count < stuct_count:
			# 					stream.read(c_ulong)
			# 					flag = stream.read(c_bit)
			# 					if flag:
			# 						stream.read(c_ulong)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					trigger = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					if trigger:
			# 						stream.read(c_longlong)
			# 					stream.read(c_ulong)
			# 					count = count + 1
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stuct_count = stream.read(c_ulong)
			# 				count = 0
			# 				while count < stuct_count:
			# 					stream.read(c_ulong)
			# 					flag = stream.read(c_bit)
			# 					if flag:
			# 						stream.read(c_ulong)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					trigger = stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					if trigger:
			# 						stream.read(c_longlong)
			# 					stream.read(c_ulong)
			# 					count = count + 1
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stream.read(c_ulong)
			# 				stream.read(c_ulong)
			# 				stream.read(c_ulong)
			# 				stream.read(c_ulong)
			# 				stream.read(c_ulong)
			# 				stream.read(c_ulong)
			# 				stream.read(c_ulong)
			# 				stream.read(c_ulong)
			# 				stream.read(c_ulong)
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				print("Current Health ", stream.read(c_ulong))
			# 				print("MaxHealth1 ", stream.read(c_float))
			# 				print("Current Armor ", stream.read(c_ulong))
			# 				print("MaxArmor1 ", stream.read(c_float))
			# 				print("Current Imagination ", stream.read(c_ulong))
			# 				print("MaxImagination1 ", stream.read(c_float))
			# 				stream.read(c_ulong)
			# 				stream.read(c_bit)
			# 				stream.read(c_bit)
			# 				stream.read(c_bit)
			# 				print("MaxHealth ", stream.read(c_float))
			# 				print("MaxArmor ", stream.read(c_float))
			# 				print("MaxImagination ", stream.read(c_float))
			# 				faction_count = stream.read(c_ulong)
			# 				count = 0
			# 				while count < faction_count:
			# 					print("Faction ", count, " ID ", stream.read(c_long))
			# 					count = count + 1
			# 				is_smashable = stream.read(c_bit)
			# 				stream.read(c_bit)
			# 				stream.read(c_bit)
			# 				if is_smashable:
			# 					stream.read(c_bit)
			# 					flag = stream.read(c_bit)
			# 					if flag:
			# 						stream.read(c_ulong)
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stream.read(c_bit)
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				flag = stream.read(c_bit)
			# 				if flag:
			# 					print("Driven vehicle ID ", stream.read(c_longlong))
			# 				stream.read(c_ubyte)
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				print("Level ", stream.read(c_ulong))
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stream.read(c_bit)
			# 				stream.read(c_bit)
			#
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				print("co ", stream.read(c_ulonglong))
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stream.read(c_ulonglong)
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stream.read(c_ulonglong)
			# 			flag = stream.read(c_bit)
			# 			if flag:
			# 				stream.read(c_ulonglong)
			# 			print("Hair Color ", stream.read(c_ulong))
			# 			print("Hair Style ", stream.read(c_ulong))
			# 			print("hd/hdc ", stream.read(c_ulong))
			# 			print("Shirt Color ", stream.read(c_ulong))
			# 			print("Pants Color ", stream.read(c_ulong))
			# 			print("cd ", stream.read(c_ulong))
			# 			print("hd/hdc ", stream.read(c_ulong))
			# 			print("Eyebrows ", stream.read(c_ulong))
			# 			print("Eyes ", stream.read(c_ulong))
			# 			print("Mouth ", stream.read(c_ulong))
			# 			print("Account ID ", stream.read(c_ulonglong))
			# 			print("Last Log ", stream.read(c_ulonglong))
			# 			stream.read(c_ulonglong)
			# 			print("Lego score ", stream.read(c_ulonglong))
			# 			print("Is free to play ", stream.read(c_bit))
			#
			# 			print("Currency collecteed ", stream.read(c_ulonglong))
			# 			print("Bricks collected ", stream.read(c_ulonglong))
			# 			print("Smashables smashed ", stream.read(c_ulonglong))
			# 			print("Quick builds completed ", stream.read(c_ulonglong))
			# 			print("Enemies smashed ", stream.read(c_ulonglong))
			# 			print("Rockets used ", stream.read(c_ulonglong))
			# 			print("Missions completed ", stream.read(c_ulonglong))
			# 			print("Pets tamed ", stream.read(c_ulonglong))
			# 			print("Imagination collected ", stream.read(c_ulonglong))
			# 			print("Life collected ", stream.read(c_ulonglong))
			# 			print("Armor collected ", stream.read(c_ulonglong))
			# 			print("Distance travelled ", stream.read(c_ulonglong))
			# 			print("Times smashed ", stream.read(c_ulonglong))
			# 			print("Damage taken ", stream.read(c_ulonglong))
			# 			print("Damage healed ", stream.read(c_ulonglong))
			# 			print("Armor repaired ", stream.read(c_ulonglong))
			# 			print("Imagination restored ", stream.read(c_ulonglong))
			# 			print("Imagination used ", stream.read(c_ulonglong))
			# 			print("Distance driven ", stream.read(c_ulonglong))
			# 			print("Airborne time", stream.read(c_ulonglong))
			# 			print("Racing imagination collected ", stream.read(c_ulonglong))
			# 			print("Racing imagination crates smashed ", stream.read(c_ulonglong))
			# 			print("Car boosts activated ", stream.read(c_ulonglong))
			# 			print("Car wrecks ", stream.read(c_ulonglong))
			# 			print("Racing smashables smashed ", stream.read(c_ulonglong))
			# 			print("Races finished ", stream.read(c_ulonglong))
			# 			print("First place races ", stream.read(c_ulonglong))
			# 			stream.read(c_bit)
			#
			# 			landing_by_rocket = stream.read(c_bit)
			# 			print("Is landing by rocket ", landing_by_rocket)
			# 			if landing_by_rocket:
			# 				rocket_count = stream.read(c_ushort)
			# 				rocket = stream.read(bytes, length=rocket_count*2)
			# 				print("Rocket ", rocket.decode('utf-16le').rstrip(' \t\r\n\0'))

			if packet_header == 0x53:
				if stream.read(c_ushort) == 0x05:
					if stream.read(c_ulong) == 0x04:
						if stream.read(c_ubyte) == 0x00:
							print("Size of following ", stream.read(c_ulong))

							is_compressed = stream.read(c_bool)
							print("Is compressed ", is_compressed)

							if is_compressed:
								print("Uncompressed size ", stream.read(c_ulong))
								compressed_size = stream.read(c_ulong)
								print("compressed size ", compressed_size)

								data = stream.read(bytes, length=compressed_size)

								print(data)


test()
