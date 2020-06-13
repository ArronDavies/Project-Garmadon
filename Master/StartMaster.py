from Master.DataTypes.Session import Session
from Master.DataTypes.MasterServer import MasterServer
from Master.DataTypes.Enums import *
from flask import Flask, request
from Master.Database import *
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')


def authenticate():
	if 'AuthCode' in request.args:
		if AuthCodeExists(request.args['AuthCode']):
			return True
		else:
			return GeneralErrorCodes.AuthCodeIncorrect.value
	else:
		return GeneralErrorCodes.NoAuthCodeSpecified.value


if __name__ == "__main__":
	if config['Settings']['DebugMode'] == 'True':
		app = Flask(__name__)
		app.config["DEBUG"] = True
	elif config['Settings']['DebugMode'] == 'False':
		app = Flask(__name__)
		app.config["DEBUG"] = False
	else:
		print('DebugMode must be "True" or "False"')

	master = MasterServer()

	@app.route('/get_sessions', methods=['GET'])
	def get_sessions():
		authorized = authenticate()

		if authorized is True:
			return master.sessions
		else:
			return {'Code': authorized}


	@app.route('/get_zones', methods=['GET'])
	def get_zones():
		authorized = authenticate()

		if authorized is True:
			return master.zones
		else:
			return {'Code': authorized}


	@app.route('/get_all', methods=['GET'])
	def get_all():
		authorized = authenticate()

		if authorized is True:
			return {'Zones': master.zones, 'Sessions': master.sessions}
		else:
			return {'Code': authorized}


	@app.route('/add_session', methods=['GET'])
	def add_session():
		authorized = authenticate()

		if authorized is True:
			if 'SessionData' in request.args:
				SessionData = json.loads(request.args['SessionData'])

				if 'ID' in SessionData:
					if 'Username' in SessionData:
						if 'Password' in SessionData:
							if UsernameExists(SessionData):
								if PasswordCorrect(SessionData):
									if AccountNotLocked(SessionData):
										if AccountNotBanned(SessionData):
											if 'IP' in SessionData:
												if 'Port' in SessionData:
													session = Session()
													session.account_id = GetAccountID(SessionData['Username'])
													session.username = SessionData['Username']
													session.password = SessionData['Password']
													session.ip = SessionData['IP']
													session.port = SessionData['Port']
													session.get_characters()
													master.sessions[SessionData['ID']] = session
												else:
													return {'Code': GeneralErrorCodes.NoPortSpecified.value}
											else:
												return {'Code': GeneralErrorCodes.NoIPSpecified.value}
										else:
											return {'Code': AccountErrorCodes.AccountBanned.value}
									else:
										return {'Code': AccountErrorCodes.AccountLocked.value}
								else:
									return {'Code': AccountErrorCodes.InvalidPassword.value}
							else:
								return {'Code': AccountErrorCodes.InvalidUsername.value}
						else:
							return {'Code': GeneralErrorCodes.NoPasswordSpecified}
					else:
						return {'Code': GeneralErrorCodes.NoUsernameSpecified}
				else:
					return {'Code': GeneralErrorCodes.NoIDSpecified}
			else:
				return {'Code': GeneralErrorCodes.NoSessionDataSpecified.value}
		else:
			return {'Code': authorized}


	app.run(host=config['Network']['OpenHost'], port=int(config['Network']['OpenPort']))
