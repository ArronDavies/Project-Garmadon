import requests
import configparser


class API:
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')

		self.AuthCode = config['Settings']['AuthCode']

		self.APIHost = config['API']['Host']
		self.APIPort = config['API']['Port']

	def get_all(self):
		return requests.get(self.APIHost + ":" + self.APIPort + "/get_all?AuthCode=" + self.AuthCode)

	def get_sessions(self):
		return requests.get(self.APIHost + ":" + self.APIPort + "/get_sessions?AuthCode=" + self.AuthCode)

	def get_zones(self):
		return requests.get(self.APIHost + ":" + self.APIPort + "/get_zones?AuthCode=" + self.AuthCode)

	def add_session(self, SessionData):
		return requests.get(self.APIHost + ":" + self.APIPort + "/get_zones?AuthCode=" + self.AuthCode + "&SessionData=" + SessionData)
