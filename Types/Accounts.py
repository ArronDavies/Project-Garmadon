import sqlite3
from Utils.GetProjectRoot import get_project_root
import bcrypt
import os


# This is more database management stuff

def createAccount(Username, Email, Password):  # Template insert ("Encry", "fake@fake.com", "password")
	if (getAccountFromUsername(Username)):
		return '{"Status": "Fail", "Reason": "Account already exists"}'
	else:
		try:
			db = sqlite3.connect(str(get_project_root()) + "/Garmadon.sqlite")
			db.row_factory = sqlite3.Row
			dbcmd = db.cursor()
			temp = Password.encode('utf-8')

			hashedPassword = bcrypt.hashpw(temp, bcrypt.gensalt())

			query = "INSERT INTO Accounts (Username, Email, Password, SessionKey, FirstLogin, Banned, Admin, CurrentCharacterID) VALUES (?,?,?,?,?,?,?,?)"
			dbcmd.execute(query, (Username, Email, hashedPassword, "", "1", "0", "1", "1"))
			db.commit()
			dbcmd.close()
			return '{"Status": "Success"}'
		except:
			return '{"Status": "Fail", "Reason": "Unknown"}'


def getAccountFromUsername(Username):  # Template insert ("Player")
	try:
		db = sqlite3.connect(str(get_project_root()) + "/Garmadon.sqlite")
		cursor = db.cursor()
		query = "select * from Accounts where Username = ?"
		cursor.execute(query, (Username,))
		data = cursor.fetchall()
		for row in data:
			id = row[0]
			Username = row[1]
			Email = row[2]
			Password = row[3]
			SessionKey = row[4]
			FirstLogin = row[5]
			Banned = row[6]
			Admin = row[7]
			CurrentCharacterID = row[8]

			jsonData = '''{"ID": id, "Username": Username, "Email": Email, "Password": Password, "SessionKey": SessionKey,
						"FirstLogin": FirstLogin,
						"Banned": Banned, "Admin": Admin, "CurrentCharacterID": CurrentCharacterID, "Status": "Success"}'''
			return jsonData
		cursor.close()
	except:
		return '{"Status": "Fail", "Reason": "Account doesn\'t exist"}'


def getAccountFromID(ID):  # Template insert (1)
	try:
		db = sqlite3.connect(str(get_project_root()) + "/Garmadon.sqlite")
		cursor = db.cursor()
		query = "select * from Accounts where id = ?"
		cursor.execute(query, (ID,))
		data = cursor.fetchall()
		for row in data:
			id = row[0]
			Username = row[1]
			Email = row[2]
			Password = row[3]
			SessionKey = row[4]
			FirstLogin = row[5]
			Banned = row[6]
			Admin = row[7]
			CurrentCharacterID = row[8]

			jsonData = '''{"ID": id, "Username": Username, "Email": Email, "Password": Password, "SessionKey": SessionKey,
						"FirstLogin": FirstLogin,
						"Banned": Banned, "Admin": Admin, "CurrentCharacterID": CurrentCharacterID, "Status": "Success"}'''
			return jsonData
		cursor.close()
	except:
		return '{"Status": "Fail", "Reason": "Account doesn\'t exist"}'


def getSpecificAccountData(Username, value):  # Template insert ("Player", "id")
	if (getAccountFromUsername(Username)):
		def switchcase(value):
			switcher = {
				"id": 0,
				"username": 1,
				"email": 2,
				"password": 3,
				"sessionKey": 4,
				"firstLogin": 5,
				"banned": 6,
				"admin": 7,
				"currentcharacterid": 8
			}
			return switcher.get(value, "Error")

		def switchcase2(value):
			switcher = {
				0: "ID",
				1: "Username",
				2: "Email",
				3: "Password",
				4: "SessionKey",
				5: "FirstLogin",
				6: "Banned",
				7: "Admin",
				8: "CurrentCharacterID"
			}
			return switcher.get(value, "Error")

		db = sqlite3.connect(str(get_project_root()) + "/Garmadon.sqlite")
		cursor = db.cursor()
		query = "select * from Accounts where Username = ?"
		cursor.execute(query, (Username,))
		data = cursor.fetchall()
		for row in data:
			if switchcase(value) == "Error":
				return '{"Status": "Fail", "Reason": "Data unreachable"}'
			else:
				return '''{"Username": Username, switchcase2(switchcase(value)): row[switchcase(value)],
						"Status": "Success"}'''
	else:
		return '{"Status": "Fail", "Reason": "Account doesn\'t exist"}'
