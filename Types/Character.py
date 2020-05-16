from Types.Inventory import Inventory
from Packets.Replica.Player import Player
from Types.Vector3 import Vector3
from Types.Vector4 import Vector4
import sqlite3
from Utils.GetProjectRoot import get_project_root


class Character:
	def __init__(self):
		self.account_id = None
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
		self.level = None
		self.u_score = None
		self.gm_level = None
		self.reputation = None

		self.x_pos = 0
		self.y_pos = 0
		self.z_pos = 0

		self.stats = None

		self.player_object = None

		self.controllable_physics_dict = {}
		self.destructible_dict = {}
		self.stats_dict = {}
		self.character_dict = {}
		self.inventory_dict = {}
		self.skill_dict = {}
		self.render_dict = {}
		self.component107_dict = {}
		self.other_data_dict = {}

	def create_player_object(self):
		self.controllable_physics_dict['IsJetpackEquipped'] = False
		self.controllable_physics_dict['JetpackEffect'] = 0
		self.controllable_physics_dict['IsJetpackInAir'] = False
		self.controllable_physics_dict['ModifyMovement'] = False
		self.controllable_physics_dict['RunSpeedMultiplier'] = 0
		self.controllable_physics_dict['GravityMultiplier'] = 0
		self.controllable_physics_dict['IsPlayer'] = True
		self.controllable_physics_dict['PlayerPos'] = Vector3(self.x_pos, self.y_pos, self.z_pos)
		self.controllable_physics_dict['PlayerRot'] = Vector4(0, 0, 0, 0)
		self.controllable_physics_dict['IsOnGround'] = True
		self.controllable_physics_dict['IsOnRail'] = False
		self.controllable_physics_dict['IsVelocity'] = False
		self.controllable_physics_dict['Velocity'] = Vector3(0, 0, 0)
		self.controllable_physics_dict['IsAngularVelocity'] = False
		self.controllable_physics_dict['AngularVelocity'] = Vector3(0, 0, 0)
		self.controllable_physics_dict['IsOnPlatform'] = False

		self.stats_dict['HasStats'] = True
		self.stats_dict['Health'] = self.health
		self.stats_dict['MaxHealth'] = self.max_health
		self.stats_dict['Armor'] = self.armor
		self.stats_dict['MaxArmor'] = self.max_armor
		self.stats_dict['Imagination'] = self.imagination
		self.stats_dict['MaxImagination'] = self.max_imagination
		self.stats_dict['DamageAbsorptionPoints'] = 0
		self.stats_dict['IsImmune'] = False
		self.stats_dict['IsGMImmune'] = False
		self.stats_dict['IsShielded'] = False
		self.stats_dict['Factions'] = []
		self.stats_dict['IsSmashable'] = False

		self.character_dict['IsOnVehicle'] = False
		self.character_dict['VehicleID'] = False
		self.character_dict['HasLevel'] = True
		self.character_dict['Level'] = self.level
		self.character_dict['AccountID'] = self.account_id
		self.character_dict['RocketModules'] = '1:9746;1:9747;1:9748'
		self.character_dict['CurrentActivity'] = 0
		self.character_dict['IsInGuild'] = False
		self.character_dict['GuildID'] = 0
		self.character_dict['GuildName'] = ""
		self.character_dict['TransitionState'] = 1
		self.character_dict['HairColor'] = self.hair_color
		self.character_dict['HairStyle'] = self.hair_style
		self.character_dict['ShirtColor'] = self.shirt_color
		self.character_dict['PantsColor'] = self.pants_color
		self.character_dict['Eyebrows'] = self.eyebrows
		self.character_dict['Eyes'] = self.eyes
		self.character_dict['Mouth'] = self.mouth
		self.character_dict['LastLog'] = 0
		self.character_dict['UScore'] = self.u_score
		self.character_dict['CurrencyCollected'] = self.stats['CurrencyCollected']
		self.character_dict['BricksCollected'] = self.stats['BricksCollected']
		self.character_dict['SmashablesSmashed'] = self.stats['SmashablesSmashed']
		self.character_dict['QuickBuildsCompleted'] = self.stats['QuickBuildsCompleted']
		self.character_dict['EnemiesSmashed'] = self.stats['EnemiesSmashed']
		self.character_dict['RocketsUsed'] = self.stats['RocketsUsed']
		self.character_dict['MissionsCompleted'] = self.stats['MissionsCompleted']
		self.character_dict['PetsTamed'] = self.stats['PetsTamed']
		self.character_dict['ImaginationPowerUpsCollected'] = self.stats['ImaginationPowerUpsCollected']
		self.character_dict['LifePowerUpsCollected'] = self.stats['LifePowerUpsCollected']
		self.character_dict['ArmorPowerUpsCollected'] = self.stats['ArmorPowerUpsCollected']
		self.character_dict['DistanceTravelled'] = self.stats['DistanceTravelled']
		self.character_dict['TimesSmashed'] = self.stats['TimesSmashed']
		self.character_dict['DamageTaken'] = self.stats['DamageTaken']
		self.character_dict['DamageHealed'] = self.stats['DamageHealed']
		self.character_dict['ArmorRepaired'] = self.stats['ArmorRepaired']
		self.character_dict['ImaginationRestored'] = self.stats['ImaginationRestored']
		self.character_dict['ImaginationUsed'] = self.stats['ImaginationUsed']
		self.character_dict['DistanceDriven'] = self.stats['DistanceDriven']
		self.character_dict['RaceCarAirborneTime'] = self.stats['RaceCarAirborneTime']
		self.character_dict['RacingImaginationPowerUpsCollected'] = self.stats['RacingImaginationPowerUpsCollected']
		self.character_dict['RacingImaginationCratesSmashed'] = self.stats['RacingImaginationCratesSmashed']
		self.character_dict['RaceCarBoostsActivated'] = self.stats['RaceCarBoostsActivated']
		self.character_dict['CarWrecks'] = self.stats['CarWrecks']
		self.character_dict['RacingSmashablesSmashed'] = self.stats['RacingSmashablesSmashed']
		self.character_dict['RacesFinished'] = self.stats['RacesFinished']
		self.character_dict['FirstPlaceRaceWins'] = self.stats['FirstPlaceRaceWins']
		self.character_dict['GMLevel'] = self.gm_level

		self.inventory_dict['HasInventory'] = True
		self.inventory_dict['Inventory'] = self.inventory

		self.other_data_dict['ObjectID'] = self.object_id
		self.other_data_dict['Name'] = self.name

		self.player_object = Player(self.controllable_physics_dict, self.destructible_dict, self.stats_dict, self.character_dict, self.inventory_dict, self.skill_dict, self.render_dict, self.component107_dict, self.other_data_dict)

	def set_last_zone(self, zone_id):
		self.last_zone = zone_id

		db = sqlite3.connect(str(get_project_root()) + "/PikaChewniverse.sqlite")
		db.row_factory = sqlite3.Row
		dbcmd = db.cursor()
		query = "UPDATE Characters SET LastZone = ? WHERE CharID = ?"
		dbcmd.execute(query, (zone_id, self.id,))
		db.commit()
		dbcmd.close()

	def set_position(self, position):
		self.x_pos = position.x
		self.y_pos = position.y
		self.z_pos = position.z

		db = sqlite3.connect(str(get_project_root()) + "/PikaChewniverse.sqlite")
		db.row_factory = sqlite3.Row
		dbcmd = db.cursor()
		query = "UPDATE Characters SET X = ?, Y = ?, Z = ? WHERE CharID = ?"
		dbcmd.execute(query, (self.x_pos, self.y_pos, self.z_pos,self.id,))
		db.commit()
		dbcmd.close()
