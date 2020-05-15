from bitstream import *
from pyraknet.replicamanager import Replica


class Character(Replica):
	def __init__(self, character_dict):
		self._is_on_vehicle = character_dict['IsOnVehicle']
		self._vehicle_id = character_dict['VehicleID']
		self._has_level = character_dict['HasLevel']
		self._level = character_dict['Level']
		self._account_id = character_dict['AccountID']
		self._rocket_modules = character_dict['RocketModules']
		self._current_activity = character_dict['CurrentActivity']
		self._in_guild = character_dict['IsInGuild']
		self._guild_id = character_dict['GuildID']
		self._guild_name = character_dict['GuildName']
		self._transition_state = character_dict['TransitionState']
		self._hair_color = character_dict['HairColor']
		self._hair_style = character_dict['HairStyle']
		self._shirt_color = character_dict['ShirtColor']
		self._pants_color = character_dict['PantsColor']
		self._eyebrows = character_dict['Eyebrows']
		self._eyes = character_dict['Eyes']
		self._mouth = character_dict['Mouth']
		self._last_log = character_dict['LastLog']
		self._u_score = character_dict['UScore']

		self._currency_collected = character_dict['CurrencyCollected']
		self._bricks_collected = character_dict['BricksCollected']
		self._smashables_smashed = character_dict['SmashablesSmashed']
		self._quick_builds_complete = character_dict['QuickBuildsCompleted']
		self._enemies_smashed = character_dict['EnemiesSmashed']
		self._rockets_used = character_dict['RocketsUsed']
		self._missions_completed = character_dict['MissionsCompleted']
		self._pets_tamed = character_dict['PetsTamed']
		self._imagination_power_ups_collected = character_dict['ImaginationPowerUpsCollected']
		self._life_power_ups_collected = character_dict['LifePowerUpsCollected']
		self._armor_power_ups_collected = character_dict['ArmorPowerUpsCollected']
		self._distance_travelled = character_dict['DistanceTravelled']
		self._times_smashed = character_dict['TimesSmashed']
		self._damage_taken = character_dict['DamageTaken']
		self._damage_healed = character_dict['DamageHealed']
		self._armor_repaired = character_dict['ArmorRepaired']
		self._imagination_restored = character_dict['ImaginationRestored']
		self._imagination_used = character_dict['ImaginationUsed']
		self._distance_driven = character_dict['DistanceDriven']
		self._race_car_airborne_time = character_dict['RaceCarAirborneTime']
		self._racing_imagination_power_ups_collected = character_dict['RacingImaginationPowerUpsCollected']
		self._racing_imagination_crates_smashed = character_dict['RacingImaginationCratesSmashed']
		self._race_car_boosts_activated = character_dict['RaceCarBoostsActivated']
		self._car_wrecks = character_dict['CarWrecks']
		self._racing_smashables_smashed = character_dict['RacingSmashablesSmashed']
		self._races_finished = character_dict['RacesFinished']
		self._first_place_wins = character_dict['FirstPlaceRaceWins']

		self._gm_level = character_dict['GMLevel']

	def part1(self, stream):
		stream.write(c_bit(True))

		stream.write(c_bit(self._is_on_vehicle))
		if self._is_on_vehicle:
			stream.write(c_longlong(self._vehicle_id))

		stream.write(c_ubyte(0))  # Unknown

	def part2(self, stream):
		stream.write(c_bit(self._has_level))
		if self._has_level:
			stream.write(c_ulong(self._level))

	def part3(self, stream):
		stream.write(c_bit(True))
		stream.write(c_bit(False))
		stream.write(c_bit(True))

	def part4(self, stream):
		stream.write(c_bit(False))  # NOTE: unknown(?)
		stream.write(c_bit(False))  # NOTE: unknown(?)
		stream.write(c_bit(False))  # NOTE: unknown(?)
		stream.write(c_bit(False))  # NOTE: unknown(?)

		stream.write(c_ulong(self._hair_color))
		stream.write(c_ulong(self._hair_style))
		stream.write(c_ulong(0))  # NOTE: unknown(?)
		stream.write(c_ulong(self._shirt_color))
		stream.write(c_ulong(self._pants_color))
		stream.write(c_ulong(0))  # NOTE: unknown(?)
		stream.write(c_ulong(0))  # NOTE: unknown(?)
		stream.write(c_ulong(self._eyebrows))
		stream.write(c_ulong(self._eyes))
		stream.write(c_ulong(self._mouth))
		stream.write(c_ulonglong(self._account_id))
		stream.write(c_ulonglong(self._last_log))
		stream.write(c_ulonglong(0))  # NOTE: unknown(?)
		stream.write(c_ulonglong(self._u_score))
		stream.write(c_bit(False))  # Free to play is a no no

		stream.write(c_ulonglong(self._currency_collected))
		stream.write(c_ulonglong(self._bricks_collected))
		stream.write(c_ulonglong(self._smashables_smashed))
		stream.write(c_ulonglong(self._quick_builds_complete))
		stream.write(c_ulonglong(self._enemies_smashed))
		stream.write(c_ulonglong(self._rockets_used))
		stream.write(c_ulonglong(self._missions_completed))
		stream.write(c_ulonglong(self._pets_tamed))
		stream.write(c_ulonglong(self._imagination_power_ups_collected))
		stream.write(c_ulonglong(self._life_power_ups_collected))
		stream.write(c_ulonglong(self._armor_power_ups_collected))
		stream.write(c_ulonglong(self._distance_travelled))
		stream.write(c_ulonglong(self._times_smashed))
		stream.write(c_ulonglong(self._damage_taken))
		stream.write(c_ulonglong(self._damage_healed))
		stream.write(c_ulonglong(self._armor_repaired))
		stream.write(c_ulonglong(self._imagination_restored))
		stream.write(c_ulonglong(self._imagination_used))
		stream.write(c_ulonglong(self._distance_driven))
		stream.write(c_ulonglong(self._race_car_airborne_time))
		stream.write(c_ulonglong(self._racing_imagination_power_ups_collected))
		stream.write(c_ulonglong(self._racing_imagination_crates_smashed))
		stream.write(c_ulonglong(self._race_car_boosts_activated))
		stream.write(c_ulonglong(self._car_wrecks))
		stream.write(c_ulonglong(self._racing_smashables_smashed))
		stream.write(c_ulonglong(self._races_finished))
		stream.write(c_ulonglong(self._first_place_wins))

		if self._transition_state == 1:
			stream.write(c_bit(True))
			stream.write(c_bit(False))
			stream.write(self._rocket_modules, length_type=c_uint16)
		elif self._transition_state == 2:
			stream.write(c_bit(False))
			stream.write(c_bit(True))
		else:
			stream.write(c_bit(False))
			stream.write(c_bit(False))

	def part5(self, stream):
		flag = True
		stream.write(c_bit(flag))
		if flag:
			stream.write(c_bit(False))  # pvp

			if self._gm_level > 0:
				stream.write(c_bit(True))
				stream.write(c_ubyte(self._gm_level))
			else:
				stream.write(c_bit(False))
				stream.write(c_ubyte(self._gm_level))

			stream.write(c_bit(False))  # NOTE: unknown
			stream.write(c_ubyte(0))  # NOTE: unknown

		if self._current_activity == 0:
			stream.write(c_bit(False))  # is not doing activity
		else:
			stream.write(c_bit(True))  # is doing activity
			stream.write(c_ulong(self._current_activity))

		stream.write(c_bit(self._in_guild))
		if self._in_guild:
			stream.write(c_longlong(self._guild_id))
			stream.write(self._guild_name, allocated_length=33)
			stream.write(c_bit(True))  # NOTE: is owner of guild?
			stream.write(c_long(-1))  # NOTE: guild creation date?

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
