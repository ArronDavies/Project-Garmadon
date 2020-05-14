from Types.Inventory import Inventory


class Character:
	def __init__(self):
		self.stats = None
		self.inventory = Inventory(self)

		self.id = None
		self.object_id = None

		self.name = None
		self.unapproved_name = None

		self.shirt_color = None
		self.shirt_style = None

		self.pants_color = None

		self.hair_style = None
		self.hair_color = None

		self.left_hand = None
		self.right_hand = None

		self.eyebrows = None
		self.eyes = None

		self.mouth = None

		self.last_zone = None

		self.health = None
		self.max_health = None

		self.armor = None
		self.max_armor = None

		self.imagination = None
		self.max_imagination = None

		self.inventory_space = None

		self.u_score = None

		self.gm_level = None
