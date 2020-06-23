import asyncio
import configparser

from bitstream import *
from event_dispatcher import EventDispatcher
from pyraknet.messages import *
from pyraknet.server import Server
from pyraknet.transports.abc import Connection, ConnectionEvent
from pyraknet.transports.raknet.connection import RaknetConnection

from Utils.Logger import GarmadonLogger, LoggingLevel


class AuthServer(Server):
	def __init__(self):
		self.logger = GarmadonLogger(LoggingLevel.AUTH)

		config = configparser.ConfigParser()
		config.read('../config.ini')
		ac = config['Auth']

		self.dispatcher = EventDispatcher()
		self.dispatcher.add_listener(Message.NewIncomingConnection, self._on_new_conn)
		self.dispatcher.add_listener(ConnectionEvent.Close, self._on_disconnect)
		self.dispatcher.add_listener(Message.UserPacket, self._on_lu_packet)

		super().__init__(address=(ac['BindIP'], int(ac['BindPort'])), max_connections=int(ac['MaxConnections']), incoming_password=b"3.25 ND1", ssl=None, dispatcher=self.dispatcher)

		self.logger.log(message="Auth server started!")

	def _on_new_conn(self, data: ReadStream, conn: Connection) -> None:
		self.logger.log(message="New Connection from: " + str(conn.get_address()))

	def _on_disconnect(self, address: RaknetConnection) -> None:
		host, port = address.get_address()
		self.logger.log(message="New Connection from: " + host + ":" + str(port))

	def _on_lu_packet(self, data: bytes, conn: Connection):
		stream = ReadStream(data); rpid = 0x53; rct = stream.read(c_ushort); pid = stream.read(c_ulong); padding = stream.read(c_ubyte)
		identifier = format(rpid, '02x') + "-" + format(rct, '02x') + "-" + format(padding, '02x') + "-" + format(pid, '02x')

		try:
			locals()[identifier]()
		except KeyError:
			self.logger.log(log_level=LoggingLevel.WARNING, message="Unhandled")


if __name__ == "__main__":
	auth = AuthServer()

	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()