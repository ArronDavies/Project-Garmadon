from AuthServer.Auth import Auth
from CharacterServer.Character import Character
from ZoneServer.Zone import Zone
import asyncio


if __name__ == "__main__":
	auth = Auth(bind_ip="0.0.0.0", port=1001, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)
	char = Character(bind_ip="0.0.0.0", port=1002, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)

	nimbus_zone = Zone(bind_ip="0.0.0.0", port=2200, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)
	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()
