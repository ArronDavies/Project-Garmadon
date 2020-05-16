from pyraknet.transports.raknet.connection import *
from uuid import uuid3, NAMESPACE_DNS


class Test:
	def __init__(self, server):
		self.name = "Test Mod"
		self.server = server

		self.listeners = []
		self.listeners.append((Message.NewIncomingConnection, self._on_connection))

	def _on_connection(self, data: ReadStream, conn: Connection) -> None:
		pass


