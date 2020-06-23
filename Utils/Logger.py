from enum import Enum


class GarmadonLogger:
	def __init__(self, default_log_level):
		self.default_log_level = default_log_level
		self.ShouldLog = True

	def log(self, log_level=None, message=None, packet=""):
		if self.ShouldLog is False:
			return

		if message is None:
			return

		if log_level is None:
			log_level = self.default_log_level

		print(log_level + "\u001b[0m" + message + LoggingLevel.PACKET + packet + "\u001b[0m")


class LoggingLevel:
	SEVERE = "\u001b[36;1m[Severe]"
	ERROR = "\u001b[31;1m[Error]"
	WARNING = "\u001b[33;1m[Warning]"
	INFO = "\u001b[32;1m[Info]"
	DEBUG = "\u001b[34;1m[Debug]"
	AUTH = "\u001b[35;1m[Auth]"
	WORLD = "\u001b[35;1m[World]"
	PACKET = "\u001b[32;1m"
