from Utils.GetProjectRoot import get_project_root
import configparser
from APIServer import app
import ctypes
from Logger import *

config = configparser.ConfigParser()
path = str(get_project_root()) + '/config.ini'
config.read(path)

def flaskThread():
	log(LOGGINGLEVEL.WEBSERVER, (" Server Started"))
	app.debug = False
	app.run(config['API']['IP'], int(config['API']['PORT']))