from bitstream import *

def SelectSkill(stream, conn, server):
	bFromSkillSet = stream.read(c_bit)
	skillID = stream.read(c_long)
	print(bFromSkillSet)
	print(skillID)