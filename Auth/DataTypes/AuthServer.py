from ssl import SSLContext
from typing import Optional

from pyraknet.messages import Address
from pyraknet.server import Server


class AuthServer(Server):
	def __init__(self, address: Address, max_connections: int, incoming_password: bytes, ssl: Optional[SSLContext]):
		super().__init__(address, max_connections, incoming_password, ssl)