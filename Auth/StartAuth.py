from Auth.DataTypes.AuthServer import AuthServer
import configparser

if __name__ == "__main__":
	config = configparser.ConfigParser()
	config.read('config.ini')

	address = (config['Network']['OpenHost'], config['Network']['OpenPort'])
	max_connections = int(config['Settings']['MaxConnections'])
	incoming_password = b"3.25 ND1"
	ssl = None

	master = AuthServer(address=address, max_connections=max_connections, incoming_password=incoming_password, ssl=ssl)