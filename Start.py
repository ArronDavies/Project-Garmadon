import asyncio
import configparser
import threading

import Logger
from AuthServer.Auth import Auth
from CLI import CLI
from CharacterServer.Character import Character
from ZoneServer.Zone import Zone

if __name__ == "__main__":
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
