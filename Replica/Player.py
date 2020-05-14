from Replica.BaseData import BaseData
from Replica.Character import Character
from Replica.ControllablePhysics import ControllablePhysics
from Replica.Destructible import Destructible
from Replica.Render import Render
from Replica.Skill import Skill
from Replica.Inventory import Inventory
from Replica.Component107 import Component107
from Replica.Stats import Stats
from Replica.Script import Script
from DataTypes import *


class Player(BaseData):
	def __init__(self, char, pos=Vector3(0, 0, 0), rot=Vector4(0, 0, 0, 0)):
		super().__init__(char["ObjectID"], 1, char["Name"])

		control = ControllablePhysics(player=True, player_pos=pos, player_rot=rot)
		render = Render()
		character = Character(shirt_color=char["ShirtColor"], hair_style=char["HairStyle"], hair_color=char["HairColor"], pants_color=char["PantsColor"], eyebrows=char["Eyebrows"], eyes=char["Eyes"], mouth=char["Mouth"], account_id=char["AccountID"])
		destructible = Destructible()
		skill = Skill()
		inventory = Inventory()
		component107 = Component107()
		stats = Stats()
		script = Script()

		self.components = [control, destructible, stats, character, inventory, skill, render, component107]