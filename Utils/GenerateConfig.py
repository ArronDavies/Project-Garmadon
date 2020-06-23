import configparser

config = configparser.ConfigParser()
config.optionxform = str

config['API'] = {'Host': '127.0.0.1', 'APILocation': '/ProjectGarmadon/backend/'}
config['Auth'] = {'BindIP': '127.0.0.1', 'BindPort': '1001', 'MaxConnections': '32'}

with open('config.ini', 'w') as configfile:
	config.write(configfile)