from Utils.GetProjectRoot import get_root
import sqlite3


def GetAccountID(Username):
	db = sqlite3.connect(str(get_root()) + "\Garmadon.sqlite")
	db.row_factory = sqlite3.Row
	db_cursor = db.cursor()

	query = "SELECT * FROM Characters WHERE AccountID = ?"
	db_cursor.execute(query, (Username,))
	value = db_cursor.fetchone()

	return value['ID']
