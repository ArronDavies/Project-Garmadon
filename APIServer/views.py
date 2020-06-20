from Types.Accounts import *
import os
from APIServer import app
from Logger import *
import logging

logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

@app.route('/')
def index():
	return ""


@app.route('/accountcreate/<username>/<email>/<password>')
def accountcreate(username, email, password):
	return createAccount(username, email, password)


@app.route('/getaccountfromusername/<username>')
def getaccountfromusername(username):
	return getAccountFromUsername(username)


@app.route('/getaccountfromid/<id>')
def getaccountfromid(id):
	return getAccountFromID(id)


@app.route('/getspecificaccountdata/<username>/<data>')
def getspecificaccountdata(username, data):
	return getSpecificAccountData(username, data)
