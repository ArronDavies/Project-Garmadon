import argparse
from Logger import *


class CLI:
	def __init__(self, world_dict):
		self.world_dict = world_dict
		self.main()

	def main(self):
		while True:
			command = input()
			if command.startswith("/help"):
				print("/tp <name> <new world id>")
				print("/tp <name> <item lot>")
			elif command.startswith("/tp"):
				args = command.split(' ')  # Note: arg[0] is the command

				char_exists = False
				for server in self.world_dict:
					for session in self.world_dict[server]._sessions:
						if self.world_dict[server]._sessions[session].current_character.name == args[1]:
							if str(args[2]) in self.world_dict:
								self.world_dict[server].transfer_world(new_world_id=args[2], session=self.world_dict[server]._sessions[session])
								char_exists = True
							else:
								char_exists = True
								log(LOGGINGLEVEL.ERROR, " That server is currently not available")
							break
				if char_exists is False:
					log(LOGGINGLEVEL.ERROR, " No user with that name exists")

			elif command.startswith("/wear_item"):
				args = command.split(' ')  # Note: arg[0] is the command
				char_exists = False
				for server in self.world_dict:
					for session in self.world_dict[server]._sessions:
						if self.world_dict[server]._sessions[session].current_character.name == args[1]:
							char_exists = True
							self.world_dict[server].add_item(item_lot=args[2], session=self.world_dict[server]._sessions[session])
							break
						else:
							char_exists = False
							break
				if char_exists is False:
					log(LOGGINGLEVEL.ERROR, " No user with that name exists")
			else:
				log(LOGGINGLEVEL.ERROR, " That command does not exist")