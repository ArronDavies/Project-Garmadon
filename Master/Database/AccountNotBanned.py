from Utils.GetProjectRoot import get_root
import sqlite3


def AccountNotBanned(SessionData):
	db = sqlite3.connect(str(get_root()) + "\Garmadon.sqlite")
	db.row_factory = sqlite3.Row
	db_cursor = db.cursor()

	query = "SELECT * FROM Accounts WHERE Username = ?"
	db_cursor.execute(query, (SessionData['Username'],))
	value = db_cursor.fetchone()
	print(value['IsBanned'])
	if value['IsBanned'] == 0:
		return True
	else:
		return False
