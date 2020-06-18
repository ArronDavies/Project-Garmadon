PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Stats
(
	CharID int,
	CurrencyCollected int default 0,
	BricksCollected int default 0,
	SmashablesSmashed int default 0,
	QuickBuildsCompleted int default 0,
	EnemiesSmashed int default 0,
	RocketsUsed int default 0,
	MissionsCompleted int default 0,
	PetsTamed int default 0,
	ImaginationPowerUpsCollected int default 0,
	LifePowerUpsCollected int default 0,
	ArmorPowerUpsCollected int default 0,
	DistanceTravelled int default 0,
	TimesSmashed int default 0,
	DamageTaken int default 0,
	DamageHealed int default 0,
	ArmorRepaired int default 0,
	ImaginationRestored int default 0,
	ImaginationUsed int default 0,
	DistanceDriven int default 0,
	RaceCarAirborneTime int default 0,
	RacingImaginationPowerUpsCollected int default 0,
	RacingImaginationCratesSmashed int default 0,
	RaceCarBoostsActivated int default 0,
	CarWrecks int default 0,
	RacingSmashablesSmashed int default 0,
	RacesFinished int default 0,
	FirstPlaceRaceWins int default 0
);
CREATE TABLE IF NOT EXISTS "Accounts"
(
	id INTEGER
		primary key autoincrement
		unique,
	Username TEXT,
	Email TEXT,
	Password TEXT,
	SessionKey int,
	FirstLogin boolean default True,
	Banned boolean default False,
	Admin boolean default False
, CurrentCharacterID int);
INSERT INTO Accounts VALUES(1,'Player','123','$2b$12$SozEPlkWaivFhBIeZGiMMuP2hqY1Zd8vOBoOpG50vUfVFze6FBNxW','',1,0,1,1);
CREATE TABLE IF NOT EXISTS "Characters"
(
	CharID INTEGER
		constraint Characters_pk
			primary key autoincrement
		unique,
	AccountID INTEGER,
	ObjectID INTEGER,
	Name TEXT,
	UnapprovedName TEXT,
	ShirtColor INTEGER,
	ShirtStyle INTEGER,
	PantsColor INTEGER,
	HairStyle INTEGER,
	HairColor INTEGER,
	LeftHand INTEGER,
	RightHand INTEGER,
	Eyebrows INTEGER,
	Eyes INTEGER,
	Mouth INTEGER,
	LastZone INTEGER default 1100,
	Health int default 4,
	MaxHealth float default 4,
	Armor int default 0,
	MaxArmor float default 0,
	Imagination int default 0,
	MaxImagination float default 0,
	InventorySpace int default 20,
	UScore int default 0,
	GMLevel int default 0,
	Reputation int default 0,
	Level int default 1,
	X float,
	Y float,
	Z float
);
CREATE TABLE IF NOT EXISTS "Inventory"
(
	CharID int,
	ItemLOT int,
	IsEquipped boolean,
	IsLinked boolean,
	Quantity int,
	Slot int,
	ItemID integer
		constraint Inventory_pk
			primary key
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Accounts',3);
INSERT INTO sqlite_sequence VALUES('Characters',23);
CREATE UNIQUE INDEX Inventory_ItemID_uindex
	on Inventory (ItemID);
COMMIT;
