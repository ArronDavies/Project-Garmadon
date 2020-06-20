from Types.Accounts import *
import os
from APIServer import app
from Logger import *
import logging
import json

logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

@app.route('/')
def index():
	return ""


@app.route('/accountcreate/<username>/<email>/<password>')
def accountcreate(username, email, password):
	data = createAccount(username, email, password)
	jsondata = json.loads(data)["Status"]
	if (jsondata == "Fail"):
		log(LOGGINGLEVEL.WEBSERVER, (" Account create failed ({}, {})").format(username, email))
	log(LOGGINGLEVEL.WEBSERVER, (" Account created ({}, {})").format(username, email))
	return data



@app.route('/getaccountfromusername/<username>')
def getaccountfromusername(username):
	log(LOGGINGLEVEL.WEBSERVER, (" {} data collected").format(username))
	return getAccountFromUsername(username)


@app.route('/getaccountfromid/<id>')
def getaccountfromid(id):
	data = json.loads(getaccountfromid(id))['Username']
	log(LOGGINGLEVEL.WEBSERVER, (" {} data collected").format(data))
	return getAccountFromID(id)


@app.route('/getspecificaccountdata/<username>/<data>')
def getspecificaccountdata(username, data):
	log(LOGGINGLEVEL.WEBSERVER, (" {} {} collected").format(username, data))
	return getSpecificAccountData(username, data)
