from bitstream import *
from Packets.Outgoing import CONSTRUCT_PACKET_HEADER


def SetJetPackMode(objid, bypass_checks=False, do_hover=False, use=False, effect_id=-1, air_speed=120.0,
				   max_air_speed=120.0, vertical_velocity=1.0, warning_effect_id=-1):
	response = WriteStream()
	CONSTRUCT_PACKET_HEADER.CONSTRUCT_PACKET_HEADER(0x53, 0x05, 0x0c, response=response)
	response.write(c_longlong(objid))
	response.write(c_ushort(0x0231))

	response.write(c_bit(bypass_checks))
	response.write(c_bit(do_hover))
	response.write(c_bit(use))

	response.write(c_long(effect_id))

	response.write(c_float(air_speed))
	response.write(c_float(max_air_speed))
	response.write(c_float(vertical_velocity))

	response.write(c_long(warning_effect_id))

	return response
