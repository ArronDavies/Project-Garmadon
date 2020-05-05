import uuid
import json


class Master:
	def __init__(self):
		self.Sessions = {}

	def create_session(self, address):
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		if uid in self.Sessions:
			return {}
		else:
			session = {'UUID': uid, 'Username': None, 'Password': None, 'Address': address, 'User Key': None, 'RCT': None, 'Current Character ID': None, 'Character Data': {}, 'First Validate Done': False}
			self.Sessions[uid] = session
			return self.Sessions[uid]

	def get_session_from_connection(self, address):  # pass in tuple (conn.get_address())
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		if uid in self.Sessions:
			return self.Sessions[uid]
		else:
			return {}

	def delete_session_from_connection(self, address):  # pass in tuple (conn.get_address())
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		self.Sessions[uid] = None
		return {}

	def get_all_sessions(self):
		return json.dumps(self.Sessions)

	def set_character_data_value_from_connection(self, id, valuetochange, newvalue, address):
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		if uid in self.Sessions:
			session = self.Sessions[uid]
			characters = session["Character Data"]
			if id in characters:
				character = characters[id]
				character[valuetochange] = newvalue
			else:
				characters[id] = {}
			return self.Sessions[uid]
		else:
			return {}

	def set_session_data_value_from_connection(self, valuetochange, newvalue, address):
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		if uid in self.Sessions:
			session = self.Sessions[uid]
			session[valuetochange] = newvalue
			return self.Sessions[uid]
		else:
			return {}

	def delete_character_from_connection(self, charid, address):  # pass in tuple (conn.get_address())
		uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))
		session = self.Sessions[uid]
		characters = session['Character Data']
		del characters[charid]
		return {}