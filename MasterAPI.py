import requests
import configparser

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
