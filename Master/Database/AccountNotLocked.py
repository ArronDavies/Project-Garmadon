from Utils.GetProjectRoot import get_root
import sqlite3


def AccountNotLocked(SessionData):
	db = sqlite3.connect(str(get_root()) + "\Garmadon.sqlite")
	db.row_factory = sqlite3.Row
	db_cursor = db.cursor()

	query = "SELECT * FROM Accounts WHERE Username = ?"
	db_cursor.execute(query, (SessionData['Username'],))
	value = db_cursor.fetchone()
	print(value['IsLocked'])
	if value['IsLocked'] == 0:
		return True
	else:
		return False
