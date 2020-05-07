import requests
import configparser
import flask

config = configparser.ConfigParser()
config.read('../config.ini')
master_info = config['MASTER']


def get_all_sessions():
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/get_all_sessions"))
	return x.text


def get_session_from_connection(ip, port):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/get_session_from_connection/" + str(ip) + "/" + str(port)))
	return x.json()


def delete_session_from_connection(ip, port):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/delete_session_from_connection/" + str(ip) + "/" + str(port)))
	return x.text


def create_session(ip, port):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/create_session/" + str(ip) + "/" + str(port)))
	return x.json()


def set_character_data_value_from_connection(id, valuetochange, newvalue, ip, port):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/set_character_data_value_from_connection/" + str(id) + "/" + str(valuetochange) + "/" + str(newvalue) + "/" + str(ip) + "/" + str(port)))
	return x


def set_session_data_value_from_connection(valuetochange, newvalue, ip, port):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/set_session_data_value_from_connection/" + str(valuetochange) + "/" + str(newvalue) + "/" + str(ip) + "/" + str(port)))
	return x.json()


def delete_character_from_connection(id, ip, port):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/delete_character_from_connection/" + str(id) + "/" + str(ip) + "/" + str(port)))
	return x.text


def get_all_zones():
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/get_all_zones"))
	return x.text


def get_zone(zone_id):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/get_zone/" + str(zone_id)))
	return x.text


def create_zone_instance(zone_id, ip, port):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/create_zone_instance/" + str(zone_id) + "/" + str(ip) + "/" + str(port)))
	return x.text


def add_session_to_instance(zone_id, instance_uuid, session_uuid):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/add_session_to_instance/" + str(zone_id) + "/" + str(instance_uuid) + "/" + str(session_uuid)))
	return x.text


def set_zone_instance_value(zone_id, instance_uuid, valuetochange, newvalue):
	x = requests.get(("http://" + master_info['Host'] + ":" + master_info['Port'] + "/set_zone_instance_value/" + str(zone_id) + "/" + str(instance_uuid) + "/" + str(valuetochange) + "/" + str(newvalue)))
	return x.text


def kick_player(host, port, uuid):
	x = requests.get(("http://" + str(host) + ":" + str(port) + "/kick_player/" + str(uuid)))
	return x.text