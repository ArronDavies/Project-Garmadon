import argparse
import os
from Logger import *
from Packets.Outgoing import *
from Types.Accounts import *
import json

class CLI:
	def __init__(self, world_dict):
		self.world_dict = world_dict

		self.commands = {}  # You can add commands here but you need to add a function under here
		self.commands['/help'] = self.handle_help
		self.commands['/tp'] = self.handle_tp
		self.commands['/fly'] = self.fly

		self.commands['/logs'] = self.logs
		self.commands['/chatlogs'] = self.chatlogs
		self.commands['/accountcreate'] = self.accountcreate
		#self.commands['/systemmessage'] = self.systemmessage

		self.main()


	def main(self):
		while True:
			command = input()
			args = command.split(' ')  # Note: arg[0] is the command
			try:
				self.commands[args[0]](args)
			except KeyError:
				log(LOGGINGLEVEL.ERROR, " That command does not exist")


	def handle_help(self, args):
		print("/tp <name> <new world id>")
		print("/fly <name>")
		print("/logs")
		print("/chatlogs")
		print("/accountcreate <username> <email> <password>")
		#print("/systemmessage <message>")


	def handle_tp(self, args):
		char_exists = False
		for server in self.world_dict:
			for session in self.world_dict[server]._sessions:
				if self.world_dict[server]._sessions[session].current_character.name == args[1]:
					if str(args[2]) in self.world_dict:
						self.world_dict[server].transfer_world(args=[1, args[2]],
															   session=self.world_dict[server]._sessions[session])
						char_exists = True
					else:
						char_exists = True
						log(LOGGINGLEVEL.ERROR, " That server is currently not available")
					break
		if char_exists is False:
			log(LOGGINGLEVEL.ERROR, " No user with that name exists")


	def handle_wear_item(self, args):
		char_exists = False
		for server in self.world_dict:
			for session in self.world_dict[server]._sessions:
				if self.world_dict[server]._sessions[session].current_character.name == args[1]:
					char_exists = True
					self.world_dict[server].wear_item(args=[1, args[2]],
													  session=self.world_dict[server]._sessions[session])
					break
				else:
					char_exists = False
		if char_exists is False:
			log(LOGGINGLEVEL.ERROR, " No user with that name exists")


	def fly(self, args):
		char_exists = False
		for server in self.world_dict:
			for session in self.world_dict[server]._sessions:
				if self.world_dict[server]._sessions[session].current_character.name == args[1]:
					char_exists = True
					self.world_dict[server].fly(session=self.world_dict[server]._sessions[session])
					break
				else:
					char_exists = False
		if char_exists is False:
			log(LOGGINGLEVEL.ERROR, " No user with that name exists")


	def chatlogs(self, args):
		if os.path.exists('chat.log'):
			with open('chat.log', 'r') as file:
				print(file.read())
		else:
			print("There are no current chat messages")


	def logs(self, args):
		if os.path.exists('Garmadon.log'):
			with open('Garmadon.log', 'r') as file:
				print(file.read())
		else:
			print("There are no current logs")

	#def systemmessage(self, args):
	#	Zone.sendmessage(args[1])

	def accountcreate(self, args):
		data = (json.loads(createAccount(args[1], args[2], args[3])))
		if data["Status"] == "Fail":
			log(LOGGINGLEVEL.CLI, (" Account create failed for reason ({})").format(data["Reason"]))
		else:
			log(LOGGINGLEVEL.CLI, (" Account created ({}, {}, {})").format(args[1], args[2], args[3]))