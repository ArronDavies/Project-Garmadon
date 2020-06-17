import asyncio
import configparser
import threading

try:
    import Logger
except:
    print("No config has been generated")
    exit(1)
try:
    from AuthServer.Auth import Auth
    from CLI import CLI
    from CharacterServer.Character import Character
    from ZoneServer.Zone import Zone
except:
    print("Essential parts of the server are missing")
    exit(1)

    
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def requirementsCheck():
    try:
        import pyraknet
    except ImportError:
        install("git+git://github.com/lcdr/pyraknet.git@259b305#egg=pyraknet")
    try:
        import bitstream
    except ImportError:
        install("git+git://github.com/lcdr/bitstream.git@b3389c8#egg=bitstream")
    try:
        import event_dispatcher
    except ImportError:
        install("git+git://github.com/lcdr/py_event_dispatcher.git@4e77404#egg=event_dispatcher")
    try:
        import requests
    except ImportError:
        install("requests")
    try:
        import bcrypt
    except ImportError:
        install("bcrypt")
    try:
        import better_profanity
    except ImportError:
        install("git+git://github.com/snguyenthanh/better_profanity.git@e352465#egg=better_profanity")

if __name__ == "__main__":
    requirementsCheck()
    Logger.logmanage()
    config = configparser.ConfigParser()
    config.read('config.ini')

    world_dict = {}
    try:
        auth = Auth(bind_ip="0.0.0.0", port=1001, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)
        char = Character(bind_ip="0.0.0.0", port=1002, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)

        zones_to_open = [1100]
        for zone in zones_to_open:
            zone_info = config[str(zone)]
            world_dict[zone] = Zone(bind_ip="0.0.0.0", port=int(zone_info['Port']), max_connections=32, incoming_password=b"3.25 ND1", ssl=None, zone_id=str(zone))

    except OSError:
        print("Ports are occupied or LUZ cannot be found")
        exit()

    cli = threading.Thread(target=CLI, args=(world_dict,))
    cli.start()

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()
