import sqlite3 as sqlite
import os


def main():
	if os.path.exists("Garmadon.sqlite"):
		pass
	else:
		f = open("Garmadon.sqlite", "w")
		f.write("")
		f.close()
	scriptfilename = "Utils/Garmadon.sql"
	dbfilename = "Garmadon.sqlite"
	connection = sqlite.connect(dbfilename)
	cursor = connection.cursor()
	scriptFile = open(scriptfilename, 'r')
	script = scriptFile.read()
	scriptFile.close()
	cursor.executescript(script)
	connection.commit()
	connection.close()
