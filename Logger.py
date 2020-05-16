import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
logging_info = config['LOGGING']

def log(logginglevel, message, packet=""):
    debug_mode = True
    debug_levels = [LOGGINGLEVEL.DEBUG, LOGGINGLEVEL.AUTHDEBUG, LOGGINGLEVEL.WORLDDEBUG, LOGGINGLEVEL.WORLDDEBUGROUTE, LOGGINGLEVEL.REPLICADEBUG, LOGGINGLEVEL.CHARACTERDEBUG, LOGGINGLEVEL.GAMEMESSAGE]

    if debug_mode is False:
        if logginglevel in debug_levels:
            pass
        else:
            print(u"" + logginglevel + LOGGINGLEVEL.PACKET + packet + LOGGINGLEVEL.MESSAGE + message)
    else:
        print(u"" + logginglevel + LOGGINGLEVEL.PACKET + packet + LOGGINGLEVEL.MESSAGE + message)
    
    if logging_info['LogOutput'] == "True":
        logging.basicConfig(level=logging.INFO, filename='pikachewniverse.log')
        logging.debug("" + LOGGINGLEVEL.PACKET + packet + LOGGINGLEVEL.MESSAGE + message)
    else:
        pass

class LOGGINGLEVEL:
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

    GAMEMESSAGE = '\u001b[36m[GAMEMESSAGE]'
    PACKET = '\u001b[37m'
    MESSAGE = '\u001b[35;1m'
    INFO = '\u001b[36m[INFO]'

