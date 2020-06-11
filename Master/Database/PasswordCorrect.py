from Utils.GetProjectRoot import get_root
import sqlite3


def PasswordCorrect(SessionData):
	db = sqlite3.connect(str(get_root()) + "\Garmadon.sqlite")
	db.row_factory = sqlite3.Row
	db_cursor = db.cursor()

	query = "SELECT * FROM Accounts WHERE Username = ?"
	db_cursor.execute(query, (SessionData['Username'],))
	value = db_cursor.fetchone()

	if SessionData['Password'] == value['Password']:
		return True
	else:
		return False
