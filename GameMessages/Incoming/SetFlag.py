from bitstream import *


def SetFlag(stream, conn, server):
    bFlag = stream.read(c_bit)
    iFlagID = stream.read(c_long)
    print(bFlag)
    print(iFlagID)
