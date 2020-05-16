def log(logginglevel, message, packet=""):
    debug_mode = False
    debug_levels = [LOGGINGLEVEL.DEBUG, LOGGINGLEVEL.AUTHDEBUG, LOGGINGLEVEL.WORLDDEBUG, LOGGINGLEVEL.WORLDDEBUGROUTE, LOGGINGLEVEL.REPLICADEBUG, LOGGINGLEVEL.CHARACTERDEBUG, LOGGINGLEVEL.GAMEMESSAGE]

    if debug_mode is False:
        if logginglevel in debug_levels:
            pass
        else:
            print(u"" + logginglevel + LOGGINGLEVEL.PACKET + packet + LOGGINGLEVEL.MESSAGE + message)
    else:
        print(u"" + logginglevel + LOGGINGLEVEL.PACKET + packet + LOGGINGLEVEL.MESSAGE + message)


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

