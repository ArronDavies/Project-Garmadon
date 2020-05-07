from Master import MasterServer
import asyncio
import configparser
import flask
from flask import *
import sqlite3
import os
import bcrypt

config = configparser.ConfigParser()
config.read('../config.ini')
master_info = config['MASTER']


if __name__ == "__main__":
	master_server = MasterServer.Master()
	app = flask.Flask(__name__)
	app.static_folder = 'static'
	app.config["DEBUG"] = True


	@app.route('/', methods=['GET', 'POST'])
	def index():
		if request.method == 'POST':
			data = request.form

			db = sqlite3.connect('../PikaChewniverse.sqlite')
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
		hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

		db = sqlite3.connect('../PikaChewniverse.sqlite')
		db.row_factory = sqlite3.Row
		dbcmd = db.cursor()
		query = "SELECT * FROM Accounts WHERE Username = ?"
		dbcmd.execute(query, (username,))
		value = dbcmd.fetchone()
		if value is not None:
			dbcmd.close()
			return {'Created': False}
		else:
			query = "INSERT INTO Accounts (Username, Email, Password) VALUES (?, ?, ?)"
			dbcmd.execute(query, (username, email, hashed,))
			db.commit()
			dbcmd.close()
			return {'Created': True}

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

	@app.route('/delete_character_from_connection/<id>/<ip>/<port>', methods=['GET'])
	def delete_character_from_connection(id, ip, port):
		return master_server.delete_character_from_connection(charid=id, address=(str(ip), int(port)))

	@app.route('/get_all_zones', methods=['GET'])
	def get_all_zones():
		return master_server.get_all_zones()

	@app.route('/get_zone/<zone_id>', methods=['GET'])
	def get_zone(zone_id):
		return master_server.get_zone(zone_id)

	@app.route('/create_zone_instance/<zone_id>/<ip>/<port>', methods=['GET'])
	def create_zone_instance(zone_id, ip, port):
		return master_server.create_zone_instance(zone_id=zone_id, address=(str(ip), int(port)))

	@app.route('/add_session_to_instance/<zone_id>/<instance_uuid>/<session_uuid>', methods=['GET'])
	def add_session_to_instance(zone_id, instance_uuid, session_uuid):
		return master_server.add_session_to_instance(zone_id=zone_id, instance_uuid=instance_uuid, session_uuid=session_uuid)

	@app.route('/set_zone_instance_value/<zone_id>/<instance_uuid>/<valuetochange>/<newvalue>', methods=['GET'])
	def set_zone_instance_value(zone_id, instance_uuid, valuetochange, newvalue):
		return master_server.set_zone_instance_value(zone_id=zone_id, instance_uuid=instance_uuid, valuetochange=valuetochange, newvalue=newvalue)


	app.run(host=master_info['Bindip'], port=master_info['Port'])
	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()
