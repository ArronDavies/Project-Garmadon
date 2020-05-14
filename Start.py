from AuthServer.Auth import Auth
from CharacterServer.Character import Character
from ZoneServer.Zone import Zone
import asyncio


if __name__ == "__main__":
	auth = Auth(bind_ip="127.0.0.1", port=1001, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)
	char = Character(bind_ip="127.0.0.1", port=1002, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)
	zone = Zone(bind_ip="127.0.0.1", port=2873, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)
	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()
