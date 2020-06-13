from Utils.GetProjectRoot import get_root
import sqlite3


def AuthCodeExists(key):
	db = sqlite3.connect(str(get_root()) + "\Garmadon.sqlite")
	db.row_factory = sqlite3.Row
	db_cursor = db.cursor()

	query = "SELECT * FROM APIKeys WHERE Key = ?"
	db_cursor.execute(query, (key,))
	value = db_cursor.fetchone()

	if value is None:
		return False
	else:
		return True