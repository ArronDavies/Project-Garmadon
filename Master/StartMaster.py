from Master.DataTypes.Session import Session
from Master.DataTypes.Enums import *
from flask import Flask, request
from Master.Database import *
import json

app = Flask(__name__)
app.config["DEBUG"] = True


class Master:
	def __init__(self):
		self.sessions = {}
		self.zones = {}

		self.start()

	def start(self):
		pass


master = Master()


@app.route('/get_sessions', methods=['GET'])
def get_sessions():
	return master.sessions


@app.route('/get_zones', methods=['GET'])
def get_zones():
	return master.zones


@app.route('/get_all', methods=['GET'])
def get_all():
	return {'Zones': master.zones, 'Sessions': master.sessions}


@app.route('/add_session', methods=['GET'])
def add_session():
	if 'SessionData' in request.args:
		SessionData = json.loads(request.args['SessionData'])

		if 'ID' in SessionData:
			if 'Username' in SessionData:
				if 'Password' in SessionData:
					if UsernameExists(SessionData):
						if PasswordCorrect(SessionData):
							if AccountNotBanned(SessionData):
								session = Session()
								session.id = SessionData['ID']
								session.username = SessionData['Username']
								session.password = SessionData['Password']

								return {'Code': AccountErrorCodes.Success.value}
							else:
								return {'Code': AccountErrorCodes.AccountBanned.value}
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


app.run()
