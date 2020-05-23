from Packets.Replica import *


class Player(BaseData.BaseData):
	def __init__(self, controllable_physics_dict, destructible_dict, stats_dict, character_dict, inventory_dict, skill_dict, render_dict, component107_dict, other_data_dict):
		super().__init__(objid=int(other_data_dict['ObjectID']), lot=1, name=other_data_dict['Name'], important=True)
		self.controllable_physics = ControllablePhysics.ControllablePhysics(controllable_physics_dict=controllable_physics_dict)
		self.destructible = Destructible.Destructible(destructible_dict=destructible_dict)
		self.stats = Stats.Stats(stats_dict=stats_dict)
		self.character = Character.Character(character_dict=character_dict)
		self.inventory = Inventory.Inventory(inventory_dict=inventory_dict)
		self.skill = Skill.Skill(skill_dict=skill_dict)
		self.render = Render.Render(render_dict=render_dict)
		self.component107 = Component107.Component107(component107_dict=component107_dict)
		self.components = [self.controllable_physics, self.destructible, self.stats, self.character, self.inventory, self.skill, self.render, self.component107]