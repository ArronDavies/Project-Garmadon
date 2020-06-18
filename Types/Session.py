import sqlite3

from Types.Character import Character
from Utils.GetProjectRoot import get_project_root


# This is more database management stuff and storing temp data on players

class Session:
	def __init__(self):
		self.ip = None
		self.port = None
		self.connection = None

		self.temp_username = None
		self.temp_password = None
		self.account_id = None
		self.username = None
		self.email = None
		self.password = None
		self.session_key = 000
		self.first_login = None
		self.is_banned = None
		self.is_admin = None

		self.first_validate = False

		self.current_character_id = None
		self.current_character = None
		self.characters = []

	def sync_account_values_down(self):
		db = sqlite3.connect(str(str(get_project_root()) + "/Garmadon.sqlite"))
		db.row_factory = sqlite3.Row

		dbcmd = db.cursor()
		query = "SELECT * FROM Accounts WHERE Username = ?"
		dbcmd.execute(query, (self.temp_username,))
		value = dbcmd.fetchone()
		dbcmd.close()
		if value is not None:
			self.account_id = value['id']
			self.username = value['Username']
			self.email = value['Email']
			self.password = value['Password']
			self.session_key = value['SessionKey']
			self.first_login = value['FirstLogin']
			self.is_banned = value['Banned']
			self.is_admin = value['Admin']
			self.current_character_id = value['CurrentCharacterID']

	def set_session_key(self, key):
		self.session_key = key

		db = sqlite3.connect(str(get_project_root()) + "/Garmadon.sqlite")
		db.row_factory = sqlite3.Row
		dbcmd = db.cursor()
		query = "UPDATE Accounts SET SessionKey = ? WHERE Username = ?"
		dbcmd.execute(query, (key, self.username,))
		db.commit()
		dbcmd.close()

	def set_current_character_id(self, charid):
		self.current_character_id = charid

		db = sqlite3.connect(str(get_project_root()) + "/Garmadon.sqlite")
		db.row_factory = sqlite3.Row
		dbcmd = db.cursor()
		query = "UPDATE Accounts SET CurrentCharacterID = ? WHERE Username = ?"
		dbcmd.execute(query, (charid, self.username,))
		db.commit()
		dbcmd.close()

	def sync_characters_down(self):
		db = sqlite3.connect(str(str(get_project_root()) + "/Garmadon.sqlite"))
		db.row_factory = sqlite3.Row

		dbcmd = db.cursor()
		query = "SELECT * FROM Characters WHERE AccountID = ?"
		dbcmd.execute(query, (self.account_id,))
		value = dbcmd.fetchall()
		dbcmd.close()
		self.characters.clear()
		if value is not None:
			for character in value:
				char = Character()
				char.account_id = character['AccountID']
				char.id = character['CharID']
				char.object_id = character['ObjectID']

				char.name = character['Name']
				char.unapproved_name = character['UnapprovedName']

				char.shirt_color = character['ShirtColor']
				char.shirt_style = character['ShirtStyle']

				char.pants_color = character['PantsColor']

				char.hair_style = character['HairStyle']
				char.hair_color = character['HairColor']

				char.left_hand = character['LeftHand']
				char.right_hand = character['RightHand']

				char.eyebrows = character['Eyebrows']
				char.eyes = character['Eyes']
				char.mouth = character['Mouth']

				char.last_zone = character['LastZone']

				char.health = character['Health']
				char.max_health = character['MaxHealth']

				char.armor = character['Armor']
				char.max_armor = character['MaxArmor']

				char.imagination = character['Imagination']
				char.max_imagination = character['MaxImagination']

				char.inventory_space = character['InventorySpace']
				char.u_score = character['UScore']
				char.gm_level = character['GMLevel']
				char.reputation = character['Reputation']
				char.level = character['Level']

				dbcmd = db.cursor()
				query = "SELECT * FROM Stats WHERE CharID = ?"
				dbcmd.execute(query, (char.id,))
				char.stats = dbcmd.fetchone()
				dbcmd.close()

				char.sync_inventory_down()
				self.characters.append(char)

	def create_character(self, character):
		db = sqlite3.connect(str(str(get_project_root()) + "/Garmadon.sqlite"))
		db.row_factory = sqlite3.Row
		dbcmd = db.cursor()

		query = "SELECT CharID FROM Characters WHERE UnapprovedName = ?"
		dbcmd.execute(query, (character['UnapprovedName'],))
		unapprovednameexists = dbcmd.fetchone()

		query = "SELECT CharID FROM Characters WHERE Name = ?"
		dbcmd.execute(query, (character['Name'],))
		nameexists = dbcmd.fetchone()

		dbcmd.close()

		if unapprovednameexists is None:
			if nameexists is None:
				db = sqlite3.connect(str(str(get_project_root()) + "/Garmadon.sqlite"))
				db.row_factory = sqlite3.Row
				dbcmd = db.cursor()
				query = "INSERT INTO Characters (AccountID, ObjectID, Name, UnapprovedName, ShirtColor, ShirtStyle, PantsColor, HairStyle, HairColor, LeftHand, RightHand, Eyebrows, Eyes, Mouth) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
				dbcmd.execute(query, (
					self.account_id, character['ObjectID'], character['Name'], character['UnapprovedName'],
					character['ShirtColor'], character['ShirtStyle'], character['PantsColor'],
					character['HairStyle'], character['HairColor'], character['LeftHand'], character['RightHand'],
					character['Eyebrows'], character['Eyes'], character['Mouth'],))
				db.commit()
				dbcmd.close()

				self.sync_characters_down()

				for char in self.characters:
					if char.name == character['Name']:
						self.current_character = char

						dbcmd = db.cursor()
						query = "INSERT INTO Stats (CharID) VALUES (?)"
						dbcmd.execute(query, (char.id,))
						db.commit()
						dbcmd.close()

				return 0x00  # Note: Success
			else:
				return 0x04  # Note: Custom name in use
		else:
			return 0x03  # Note: Unapproved name in use
