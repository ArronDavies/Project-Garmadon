from bitstream import *
from pyraknet.replicamanager import Replica


class Character(Replica):
	def __init__(self, vehicle=False, vehicle_id=0, level=True, level_num=1, hair_color=0, hair_style=0, shirt_color=0, pants_color=0, eyebrows=0, eyes=0, mouth=0, account_id=1, llog=0, lego_score=0, free_to_play=False, currency_collected=0, bricks_collected=0, smashables_smashed=0, quick_builds=0, enemies_smashed=0, rockets_used=0, missions_completed=0, pets_tamed=0, imagination_powerups=0, life_powerups=0, armor_powerups=0, distance_traveled=0, times_smashed=0, damage_taken=0, damage_healed=0, armor_repaired=0, imagination_restored=0, imagination_used=0, distance_driven=0, airborne_time_race_car=0, racing_imagination_powerups=0, racing_imagination_crates_smashed=0, race_car_boosts=0, race_car_wrecks=0, racing_smashables_smashed=0, races_finished=0, first_place_finishes=0, rocket=False, rocket_characters=0, rocket_modules=[''], activity=False, activity_id=0, guild=False, guild_id=0, guild_name='', pvp=False, gm=False, gmlevel=0):
		self.vehicle = vehicle
		self.vehicle_id = vehicle_id
		self.level = level
		self.level_num = level_num
		self.hair_color = hair_color
		self.hair_style = hair_style
		self.shirt_color = shirt_color
		self.pants_color = pants_color
		self.eyebrows = eyebrows
		self.eyes = eyes
		self.mouth = mouth
		self.account_id = account_id
		self.llog = llog
		self.lego_score = lego_score
		self.free_to_play = free_to_play
		self.currency_collected = currency_collected
		self.bricks_collected = bricks_collected
		self.smashables_smashed = smashables_smashed
		self.quick_builds = quick_builds
		self.enemies_smashed = enemies_smashed
		self.rockets_used = rockets_used
		self.missions_completed = missions_completed
		self.pets_tamed = pets_tamed
		self.imagination_powerups = imagination_powerups
		self.life_powerups = life_powerups
		self.armor_powerups = armor_powerups
		self.distance_traveled = distance_traveled
		self.times_smashed = times_smashed
		self.damage_taken = damage_taken
		self.damage_healed = damage_healed
		self.armor_repaired = armor_repaired
		self.imagination_restored = imagination_restored
		self.imagination_used = imagination_used
		self.distance_driven = distance_driven
		self.airborne_time_race_car = airborne_time_race_car
		self.racing_imagination_powerups = racing_imagination_powerups
		self.racing_imagination_crates_smashed = racing_imagination_crates_smashed
		self.race_car_boosts = race_car_boosts
		self.race_car_wrecks = race_car_wrecks
		self.racing_smashables_smashed = racing_smashables_smashed
		self.races_finished = races_finished
		self.first_place_finishes = first_place_finishes
		self.rocket = rocket
		self.rocket_characters = rocket_characters
		self.rocket_modules = rocket_modules
		self.activity = activity
		self.activity_id = activity_id
		self.guild = guild
		self.guild_id = guild_id
		self.guild_name = guild_name
		self.pvp = pvp
		self.gm = gm
		self.gmlevel = gmlevel



	def part1(self, stream):
		stream.write(c_bit(True))

		stream.write(c_bit(self.vehicle))
		if self.vehicle:
			stream.write(c_longlong(self.vehicle_id))

		stream.write(c_ubyte(0))  # Unknown

	def part2(self, stream):
		stream.write(c_bit(self.level))

		if self.level:
			stream.write(c_ulong(self.level_num))

	def part3(self, stream):
		stream.write(c_bit(True))
		stream.write(c_bit(False))
		stream.write(c_bit(True))

	# Creation only
	def part4(self, stream):
		stream.write(c_bit(False))  # NOTE: unknown flag(?)
		stream.write(c_bit(False))  # NOTE: unknown flag
		stream.write(c_bit(False))  # NOTE: same as above
		stream.write(c_bit(False))  # NOTE: same here

		stream.write(c_ulong(self.hair_color))
		stream.write(c_ulong(self.hair_style))
		stream.write(c_ulong(0))  # NOTE: unknown(?)
		stream.write(c_ulong(self.shirt_color))
		stream.write(c_ulong(self.pants_color))
		stream.write(c_ulong(0))  # NOTE: unknown(?)
		stream.write(c_ulong(0))  # NOTE: unknown(?)
		stream.write(c_ulong(self.eyebrows))
		stream.write(c_ulong(self.eyes))
		stream.write(c_ulong(self.mouth))

		stream.write(c_ulonglong(self.account_id))
		stream.write(c_ulonglong(self.llog))
		stream.write(c_ulonglong(0))  # NOTE: unknown
		stream.write(c_ulonglong(self.lego_score))

		stream.write(c_bit(self.free_to_play))

		stream.write(c_ulonglong(self.currency_collected))
		stream.write(c_ulonglong(self.bricks_collected))
		stream.write(c_ulonglong(self.smashables_smashed))
		stream.write(c_ulonglong(self.quick_builds))
		stream.write(c_ulonglong(self.enemies_smashed))
		stream.write(c_ulonglong(self.rockets_used))
		stream.write(c_ulonglong(self.missions_completed))
		stream.write(c_ulonglong(self.pets_tamed))
		stream.write(c_ulonglong(self.imagination_powerups))
		stream.write(c_ulonglong(self.life_powerups))
		stream.write(c_ulonglong(self.armor_powerups))
		stream.write(c_ulonglong(self.distance_traveled))
		stream.write(c_ulonglong(self.times_smashed))
		stream.write(c_ulonglong(self.damage_taken))
		stream.write(c_ulonglong(self.damage_healed))
		stream.write(c_ulonglong(self.armor_repaired))
		stream.write(c_ulonglong(self.imagination_restored))
		stream.write(c_ulonglong(self.imagination_used))
		stream.write(c_ulonglong(self.distance_driven))
		stream.write(c_ulonglong(self.airborne_time_race_car))
		stream.write(c_ulonglong(self.racing_imagination_powerups))
		stream.write(c_ulonglong(self.racing_imagination_crates_smashed))
		stream.write(c_ulonglong(self.race_car_boosts))
		stream.write(c_ulonglong(self.race_car_wrecks))
		stream.write(c_ulonglong(self.racing_smashables_smashed))
		stream.write(c_ulonglong(self.races_finished))
		stream.write(c_ulonglong(self.first_place_finishes))

		stream.write(c_bit(False))  # NOTE: unknown(?)

		stream.write(c_bit(self.rocket))

		if self.rocket:
			stream.write(c_ushort(self.rocket_characters))

	# post creation
	def part5(self, stream):
		flag = True
		stream.write(c_bit(flag))
		if flag:
			stream.write(c_bit(self.pvp))
			stream.write(c_bit(self.gm))
			stream.write(c_ubyte(self.gmlevel))
			stream.write(c_bit(False))  # NOTE: unknown
			stream.write(c_ubyte(0))  # NOTE: unknown

		stream.write(c_bit(self.activity))
		if self.activity:
			stream.write(c_ulong(self.activity_id))

		stream.write(c_bit(self.guild))
		if self.guild:
			stream.write(c_longlong(self.guild_id))
			stream.write(self.guild_name, allocated_length=33)
			stream.write(c_bit(True))  # NOTE: unknown
			stream.write(c_long(-1))  # NOTE: unknown

	def write_construction(self, stream: WriteStream) -> None:
		self.part1(stream)
		self.part2(stream)
		self.part3(stream)
		self.part4(stream)  # Creation
		self.part5(stream)  # Post creation

	def serialize(self, stream: WriteStream) -> None:
		self.part1(stream)
		self.part2(stream)
		self.part3(stream)
		self.part5(stream)  # Post creation

	def on_destruction(self) -> None:
		raise NotImplementedError