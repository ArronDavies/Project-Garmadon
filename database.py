import sqlite3

db = sqlite3.connect('../PikaChewniverse.sqlite')
db.row_factory = sqlite3.Row


def get_account_data_from_username(var):
    dbcmd = db.cursor()
    query = "SELECT * FROM Accounts WHERE Username = ?"
    dbcmd.execute(query, (var,))
    value = dbcmd.fetchone()
    dbcmd.close()
    if value is not None:
        return value
    else:
        return None


def get_character_data_from_accountid(var):
    dbcmd = db.cursor()
    query = "SELECT * FROM Characters WHERE AccountID = ?"
    dbcmd.execute(query, (var,))
    value = dbcmd.fetchall()
    dbcmd.close()
    return value


def check_if_minifig_name_exists(var):
    dbcmd = db.cursor()
    query = "SELECT CharID FROM Characters WHERE UnapprovedName = ?"
    dbcmd.execute(query, (var,))
    value = dbcmd.fetchone()
    dbcmd.close()
    return value


def create_character(AccountID, ObjectID, Name, UnapprovedName, ShirtColor, ShirtStyle, PantsColor, HairStyle,
                     HairColor, LeftHand, RightHand, Eyebrows, Eyes, Mouth):
    dbcmd = db.cursor()
    query = "INSERT INTO Characters (AccountID, ObjectID, Name, UnapprovedName, ShirtColor, ShirtStyle, PantsColor, HairStyle, HairColor, LeftHand, RightHand, Eyebrows, Eyes, Mouth) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    dbcmd.execute(query, (
    AccountID, ObjectID, Name, UnapprovedName, ShirtColor, ShirtStyle, PantsColor, HairStyle, HairColor, LeftHand, RightHand,
    Eyebrows, Eyes, Mouth,))
    db.commit()
    dbcmd.close()


def get_character_data_from_objid(var):
    dbcmd = db.cursor()
    query = "SELECT * FROM Characters WHERE ObjectID = ?"
    dbcmd.execute(query, (var,))
    value = dbcmd.fetchone()
    dbcmd.close()
    return value


def set_account_currentcharacter_from_id(characterid, accountid):
    dbcmd = db.cursor()
    query = "UPDATE Accounts SET CurrentCharacter = ? WHERE id = ?"
    dbcmd.execute(query, (characterid, accountid,))
    db.commit()
    dbcmd.close()


def delete_character_from_objectid(var):
    dbcmd = db.cursor()
    query = "DELETE From Characters WHERE ObjectID = ?"
    dbcmd.execute(query, (var,))
    dbcmd.close()


def set_character_name_from_objectid(name, id):
    dbcmd = db.cursor()
    query = "UPDATE Characters SET Name = ? WHERE ObjectID = ?"
    dbcmd.execute(query, (name, id,))
    db.commit()
    dbcmd.close()


def get_account_data_from_email(var):
    dbcmd = db.cursor()
    query = "SELECT * FROM Accounts WHERE Email = ?"
    dbcmd.execute(query, (var,))
    value = dbcmd.fetchone()
    dbcmd.close()
    if value is not None:
        return value
    else:
        return None


def create_account(Email, Username, Password):
    dbcmd = db.cursor()
    query = "INSERT INTO Accounts (Username, Email, Password) VALUES (?, ?, ?)"
    dbcmd.execute(query, (Username, Email, Password,))
    db.commit()
    dbcmd.close()
