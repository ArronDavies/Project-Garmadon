
class Session:
	def __init__(self):
		self.id = None
		self.username = None
		self.password = None

		self.session_key = None
		self.characters = {}

		self.ip = None
		self.port = None