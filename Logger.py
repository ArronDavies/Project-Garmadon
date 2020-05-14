
def log(logginglevel, message, packet=""):
    print(u"" + logginglevel + LOGGINGLEVEL.PACKET + packet + LOGGINGLEVEL.MESSAGE + message)
    # TODO: Write to file


class LOGGINGLEVEL:
    WARNING = '\u001b[33m[WARNING]'
    ERROR = '\u001b[31m[ERROR]'
    DEBUG = '\u001b[34m[DEBUG]'
    AUTHDEBUG = '\u001b[31m[DEBUG][AUTH]'
    WORLDDEBUG = '\u001b[34m[DEBUG][WORLD]'
    REPLICADEBUG = '\u001b[34m[DEBUG][REPLICA]'
    CHARACTERDEBUG = '\u001b[32m[DEBUG][CHARACTER]'
    GAMEMESSAGE = '\u001b[36m[GAMEMESSAGE]'
    PACKET = '\u001b[37m'
    MESSAGE = '\u001b[35;1m'
    INFO = '\u001b[36m[INFO]'

