import argparse

class CLI:
	def __init__(self, world_dict):
		self.world_dict = world_dict
		self.main()

	def main(self):
		while True:
			command = input()
			if command.startswith("/help"):
				print("/tp <name> <new world id>")
			elif command.startswith("/tp"):
				args = command.split(' ')  # Note: arg[0] is the command

				exists = False
				for server in self.world_dict:
					for session in self.world_dict[server]._sessions:
						if self.world_dict[server]._sessions[session].current_character.name == args[1]:
							self.world_dict[server].transfer_world(new_world_id=args[2], session=self.world_dict[server]._sessions[session])
							exists = True
							break
				if exists is False:
					print("No user with that name exists")
			else:
				print("That command does not exist")