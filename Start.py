from AuthServer.Auth import Auth
from CharacterServer.Character import Character
from ZoneServer.Zone import Zone
import asyncio
from CLI import CLI
import threading
from Mods import Test

import os
import shutil
from datetime import datetime
from pathlib import Path

def logmanage():
    if os.path.exists("Logs"):
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
        if os.path.exists("pikachewniverse.log"):
            now = datetime.now()
            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
            shutil.move((str(Path.cwd()) + r"\pikachewniverse.log"), (str(Path.cwd()) + "\Logs\\"))
            os.rename((str(Path.cwd()) + r"\Logs\pikachewniverse.log"),(str(Path.cwd()) + "\Logs\\" + dt_string + ".log"))
        else:
            pass
    else:
        os.mkdir("Logs")

if __name__ == "__main__":
    logmanage()
    world_dict = {}
    auth = Auth(bind_ip="0.0.0.0", port=1001, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)
    char = Character(bind_ip="0.0.0.0", port=1002, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)

    nimbus_zone = Zone(bind_ip="0.0.0.0", port=2200, max_connections=32, incoming_password=b"3.25 ND1", ssl=None, zone_id="1200")
    world_dict['1200'] = nimbus_zone


    cli = threading.Thread(target=CLI, args=(world_dict,))
    cli.start()

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()
