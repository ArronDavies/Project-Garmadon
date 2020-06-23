import logging
import configparser
import os
import shutil
from datetime import datetime
from pathlib import Path
import psutil
import os

config = configparser.ConfigParser()
config.read('config.ini')
logging_info = config['LOGGING']


def log(logginglevel, message, packet=""):
	debug_mode = True
	debug_levels = [LOGGINGLEVEL.DEBUG, LOGGINGLEVEL.AUTHDEBUG, LOGGINGLEVEL.WORLDDEBUG, LOGGINGLEVEL.WORLDDEBUGROUTE,
					LOGGINGLEVEL.REPLICADEBUG, LOGGINGLEVEL.CHARACTERDEBUG, LOGGINGLEVEL.GAMEMESSAGE]

	if debug_mode is False:
		if logginglevel in debug_levels:
			pass
		else:
			print(u"" + logginglevel + LOGGINGLEVEL.PACKET + packet + LOGGINGLEVEL.MESSAGE + message)
	else:
		print(u"" + logginglevel + LOGGINGLEVEL.PACKET + packet + LOGGINGLEVEL.MESSAGE + message)

	f = open('Garmadon.log', 'a')
	f.write(logginglevel[5:] + message + "\n")
	f.close()

def logmanage():
	if os.path.exists("Logs"):
		if os.path.exists("Logs/Garmadon.log"):
			os.remove("Logs/Garmadon.log")
		dir = (str(Path.cwd()) + '\\Logs')
		if (len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])) > 19:
			try:
				shutil.rmtree('Logs')
				os.mkdir('Logs')
			except:
				pass
		else:
			pass
		if os.path.exists("Logs"):
			pass
		else:
			os.chdir("Logs")
		if os.path.exists("Garmadon.log"):
			now = datetime.now()
			dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
			shutil.move((str(Path.cwd()) + r"\Garmadon.log"), (str(Path.cwd()) + "\Logs\\"))
			os.rename((str(Path.cwd()) + r"\Logs\Garmadon.log"), (str(Path.cwd()) + "\Logs\\" + dt_string + ".log"))
		else:
			pass
	else:
		os.mkdir("Logs")


def chatlogmanage():
	if os.path.exists("ChatLogs"):
		dir = (str(Path.cwd()) + '\\ChatLogs')
		if (len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])) > 19:
			shutil.rmtree('ChatLogs')
			os.mkdir('ChatLogs')
		else:
			pass
		if os.path.exists("chat.log"):
			now = datetime.now()
			dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
			os.rename((str(Path.cwd()) + r"\\chat.log"), (str(Path.cwd()) + "\ChatLogs\\" + dt_string + ".log"))
		else:
			pass
	else:
		os.mkdir("ChatLogs")


class LOGGINGLEVEL:
	try:
		ppid = os.getppid()  # Find parent process pid
		value = psutil.Process(ppid).name()  # Get exe name of that process
	except:  # Just so that using this on Linux and Mac doesn't break it
		value = "noansi"
	if value == "cmd.exe":
		WARNING = '[WARNING]'
		ERROR = '[ERROR]'
		DEBUG = '[DEBUG]'
		AUTHDEBUG = '[DEBUG][AUTH]'
		WORLDDEBUG = '[DEBUG][WORLD]'
		WORLDDEBUGROUTE = '[WORLD][ROUTE]'
		REPLICADEBUG = '[DEBUG][REPLICA]'
		CHARACTERDEBUG = '[DEBUG][CHARACTER]'

		AUTH = '[AUTH]'
		WORLD = '[WORLD]'
		REPLICA = '[REPLICA]'
		CHARACTER = '[CHARACTER]'
		WEBSERVER = '[WEBSERVER]'
		CLI = '[CLI]'

		GAMEMESSAGE = '[GAMEMESSAGE]'
		PACKET = ''
		MESSAGE = ''
		INFO = '[INFO]'
	elif value == "powershell.exe":
		WARNING = '[WARNING]'
		ERROR = '[ERROR]'
		DEBUG = '[DEBUG]'
		AUTHDEBUG = '[DEBUG][AUTH]'
		WORLDDEBUG = '[DEBUG][WORLD]'
		WORLDDEBUGROUTE = '[WORLD][ROUTE]'
		REPLICADEBUG = '[DEBUG][REPLICA]'
		CHARACTERDEBUG = '[DEBUG][CHARACTER]'

		AUTH = '[AUTH]'
		WORLD = '[WORLD]'
		REPLICA = '[REPLICA]'
		CHARACTER = '[CHARACTER]'
		WEBSERVER = '[WEBSERVER]'
		CLI = '[CLI]'

		GAMEMESSAGE = '[GAMEMESSAGE]'
		PACKET = ''
		MESSAGE = ''
		INFO = '[INFO]'
	elif value == "noansi":
		WARNING = '[WARNING]'
		ERROR = '[ERROR]'
		DEBUG = '[DEBUG]'
		AUTHDEBUG = '[DEBUG][AUTH]'
		WORLDDEBUG = '[DEBUG][WORLD]'
		WORLDDEBUGROUTE = '[WORLD][ROUTE]'
		REPLICADEBUG = '[DEBUG][REPLICA]'
		CHARACTERDEBUG = '[DEBUG][CHARACTER]'

		AUTH = '[AUTH]'
		WORLD = '[WORLD]'
		REPLICA = '[REPLICA]'
		CHARACTER = '[CHARACTER]'
		WEBSERVER = '[WEBSERVER]'
		CLI = '[CLI]'

		GAMEMESSAGE = '[GAMEMESSAGE]'
		PACKET = ''
		MESSAGE = ''
		INFO = '[INFO]'
	else:
		WARNING = '\u001b[33m[WARNING]'
		ERROR = '\u001b[31m[ERROR]'
		DEBUG = '\u001b[34m[DEBUG]'
		AUTHDEBUG = '\u001b[32m[DEBUG][AUTH]'
		WORLDDEBUG = '\u001b[34m[DEBUG][WORLD]'
		WORLDDEBUGROUTE = '\u001b[34m[WORLD][ROUTE]'
		REPLICADEBUG = '\u001b[34m[DEBUG][REPLICA]'
		CHARACTERDEBUG = '\u001b[30m[DEBUG][CHARACTER]'

		AUTH = '\u001b[32m[AUTH]'
		WORLD = '\u001b[34m[WORLD]'
		REPLICA = '\u001b[34m[REPLICA]'
		CHARACTER = '\u001b[30m[CHARACTER]'
		WEBSERVER = '\u001b[34m[WEBSERVER]'
		CLI = '\u001b[34m[CLI]'

		GAMEMESSAGE = '\u001b[36m[GAMEMESSAGE]'
		PACKET = '\u001b[37m'
		MESSAGE = '\u001b[35;1m'
		INFO = '\u001b[36m[INFO]'