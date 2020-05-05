from Master import MasterServer
import asyncio
import configparser
import flask
from flask import *
import sqlite3
import os
import bcrypt
import database

config = configparser.ConfigParser()
config.read('../config.ini')
master_info = config['MASTER']

project_root = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(project_root, 'PikaChewniverse.sqlite')


if __name__ == "__main__":
	master_server = MasterServer.Master()
	app = flask.Flask(__name__)
	app.static_folder = 'static'
	app.config["DEBUG"] = True


	@app.route('/', methods=['GET', 'POST'])
	def index():
		if request.method == 'POST':
			data = request.form

			db = sqlite3.connect(db_path)
			db.row_factory = sqlite3.Row
			dbcmd = db.cursor()
			query = "SELECT * FROM Accounts WHERE Email = ?"
			dbcmd.execute(query, (data['email'],))
			value = dbcmd.fetchone()
			dbcmd.close()

			if value is not None:
				if bcrypt.checkpw(data['password'].encode('utf-8'), value['Password'].encode('utf-8')):
					return render_template(r"admin.html")
				else:
					return render_template(r"index.html")
			else:
				return render_template(r"index.html")
		else:
			return render_template(r"index.html")

	@app.route('/create_account/<email>/<username>/<password>', methods=['GET'])
	def create_account(email, username, password):
		salt = bcrypt.gensalt()
		hashed = bcrypt.hashpw(password, salt)
		database.create_account(email, username, hashed)
		return {}

	@app.route('/get_all_sessions', methods=['GET'])
	def get_all_sessions():
		return master_server.get_all_sessions()

	@app.route('/get_session_from_connection/<ip>/<port>', methods=['GET'])
	def get_session_from_connection(ip, port):
		return master_server.get_session_from_connection((str(ip), int(port)))

	@app.route('/delete_session_from_connection/<ip>/<port>', methods=['GET'])
	def delete_session_from_connection(ip, port):
		return master_server.get_session_from_connection((str(ip), int(port)))

	@app.route('/create_session/<ip>/<port>', methods=['GET'])
	def create_session(ip, port):
		return master_server.create_session(address=(str(ip), int(port)))

	@app.route('/set_character_data_value_from_connection/<id>/<valuetochange>/<newvalue>/<ip>/<port>', methods=['GET'])
	def set_character_data_value_from_connection(id, valuetochange, newvalue, ip, port):
		return master_server.set_character_data_value_from_connection(id=id, valuetochange=valuetochange, newvalue=newvalue, address=(str(ip), int(port)))

	@app.route('/set_session_data_value_from_connection/<valuetochange>/<newvalue>/<ip>/<port>', methods=['GET'])
	def set_session_data_value_from_connection(valuetochange, newvalue, ip, port):
		return master_server.set_session_data_value_from_connection(valuetochange=valuetochange, newvalue=newvalue, address=(str(ip), int(port)))


	app.run(host=master_info['Bindip'], port=master_info['Port'])
	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()
