import uuid
import json
import flask
import upnpy

class Master:
	def __init__(self):
		self.Sessions = {}
		self.Zones = {}

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

	def get_all_zones(self):
		return self.Zones

	def get_zone(self, zone_id):
		if zone_id in self.Zones:
			return self.Zones[zone_id]
		else:
			return {}

	def create_zone_instance(self, zone_id, address):
		zone_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(address)))

		if zone_id in self.Zones:
			zone = self.Zones[zone_id]
			if zone_uuid in zone:
				return zone[zone_uuid]
			else:
				zone[zone_uuid] = {'IP': address[0], 'Port': address[1], 'Sessions': [], 'Players': 0}
				return zone[zone_uuid]
		else:
			self.Zones[zone_id] = {zone_uuid: {'IP': address[0], 'Port': address[1], 'Sessions': [], 'Players': 0}}
			return self.Zones[zone_id]

		upnp = upnpy.UPnP()
		try:
			device = upnp.get_igd()
			device.get_services()
			service = device['WANPPPConnection.1']
			service.get_actions()
			service.AddPortMapping.get_input_arguments()
			service.AddPortMapping(
				NewRemoteHost='',
				NewExternalPort=address[1],
				NewProtocol='TCP',
				NewInternalPort=address[1],
				NewInternalClient=address[0],
				NewEnabled=1,
				NewPortMappingDescription='PikaChewniverse Zone Server',
				NewLeaseDuration=0
			)
		except upnpy.exceptions.IGDError:
			print("No UPNP available device found")

	def add_session_to_instance(self, zone_id, instance_uuid, session_uuid):
		if zone_id in self.Zones:
			if instance_uuid in self.Zones[zone_id]:
				if session_uuid in self.Zones[zone_id][instance_uuid]['Sessions']:
					return self.Zones[zone_id][instance_uuid]['Sessions']
				else:
					self.Zones[zone_id][instance_uuid]['Sessions'].append(session_uuid)
					return self.Zones[zone_id][instance_uuid]['Sessions']
			else:
				return {}
		else:
			return {}

	def set_zone_instance_value(self, zone_id, instance_uuid, valuetochange, newvalue):
		if zone_id in self.Zones:
			if instance_uuid in self.Zones[zone_id]:
				self.Zones[zone_id][instance_uuid][valuetochange] = newvalue
				return self.Zones[zone_id][instance_uuid]
			else:
				return {}
		else:
			return {}

