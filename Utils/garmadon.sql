pragma foreign_keys=off;
begin transaction;
create table Stats
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
create table if not exists "Accounts"
(
	id integer
		primary key autoincrement
		unique,
	Username text,
	Email text,
	Password text,
	SessionKey int,
	FirstLogin boolean default True,
	Banned boolean default False,
	Admin boolean default False
, CurrentCharacterID int);
insert into Accounts values(1,'Player','123','$2b$12$SozEPlkWaivFhBIeZGiMMuP2hqY1Zd8vOBoOpG50vUfVFze6FBNxW','',1,0,1,1);
create table if not exists "Characters"
(
	CharID integer
		constraint Characters_pk
			primary key autoincrement
		unique,
	AccountID integer,
	ObjectID integer,
	Name text,
	UnapprovedName text,
	ShirtColor integer,
	ShirtStyle integer,
	PantsColor integer,
	HairStyle integer,
	HairColor integer,
	LeftHand integer,
	RightHand integer,
	Eyebrows integer,
	Eyes integer,
	Mouth integer,
	LastZone integer default 1100,
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
create table if not exists "Inventory"
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
commit;