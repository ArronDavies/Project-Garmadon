from Master.Database import *


class Session:
	def __init__(self):
		self.account_id = None
		self.username = None
		self.password = None

		self.characters = {}

		self.ip = None
		self.port = None

	def get_characters(self):
		characters = GetCharacters(self.account_id)
		character = {}