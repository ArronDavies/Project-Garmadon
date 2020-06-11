import enum


class AccountErrorCodes(enum.IntEnum):
	GeneralFailed = 0x00
	Success = 0x01,
	AccountBanned = 0x02,
	PermissionsNotHighEnough = 0x05,
	InvalidPassword = 0x06,
	AccountLocked = 0x07,
	InvalidUsername = 0x08,
	ActivationPending = 0x09,
	AccountDisabled = 0x0a,
	GameTimeExpired = 0x0b,
	TrialEnded = 0x0c,
	PlaySchedule = 0x0d,
	AccountNotActivated = 0x0e,

	# Note 0x0f > 0xff and anything else not done below


# Note: Don't assign anything equal to or below 255(0XFF)
class GeneralErrorCodes(enum.IntEnum):
	NoSessionDataSpecified = 0xFFFF,
	NoIDSpecified = 0XFFFE,
	NoUsernameSpecified = 0XFFFD,
	NoPasswordSpecified = 0XFFFc
