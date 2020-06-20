import os
import Utils.GetProjectRoot
import socket


def write():
	f = open("config.ini", "a")
	f.write("\n;This is a config file for the Garmadon settings.")
	f.write("\n")
	f.write("\n[CHARACTER]")
	f.write("\nHost = 127.0.0.1")
	f.write("\nPort = 1002")
	f.write("\n")
	f.write("\n[AUTH]")
	f.write("\nHost = 127.0.0.1")
	f.write("\nPort = 1001")
	f.write("\n")
	f.write("\n[1100]")
	f.write("\nHost = 127.0.0.1")
	f.write("\nPort = 2100")
	f.write("\nLUZ = /clientfiles/maps/01_live_maps/avant_gardens/nd_avant_gardens.luz")
	f.write("\nLVL = /clientfiles/maps/01_live_maps/avant_gardens/")
	f.write("\n")
	f.write("\n[LOGGING]")
	f.write("\nLogOutput = True")
	f.write("\n")
	f.write("\n[API]")
	f.write("\nIP = 127.0.0.1")
	f.write("\nPort = 8080")
	f.write("\n")
	f.close()