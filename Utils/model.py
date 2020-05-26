from sqlalchemy import Boolean, Column, Float, Integer, Table, Text, text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

class Account(Base):
    __tablename__ = 'Accounts'

    id = Column(Integer, primary_key=True)
    Username = Column(Text)
    Email = Column(Text)
    Password = Column(Text)
    SessionKey = Column(Integer)
    FirstLogin = Column(Boolean, server_default=text("True"))
    Banned = Column(Boolean, server_default=text("False"))
    Admin = Column(Boolean, server_default=text("False"))
    CurrentCharacterID = Column(Integer)


class Character(Base):
    __tablename__ = 'Characters'

    CharID = Column(Integer, primary_key=True)
    AccountID = Column(Integer)
    ObjectID = Column(Integer)
    Name = Column(Text)
    UnapprovedName = Column(Text)
    ShirtColor = Column(Integer)
    ShirtStyle = Column(Integer)
    PantsColor = Column(Integer)
    HairStyle = Column(Integer)
    HairColor = Column(Integer)
    LeftHand = Column(Integer)
    RightHand = Column(Integer)
    Eyebrows = Column(Integer)
    Eyes = Column(Integer)
    Mouth = Column(Integer)
    LastZone = Column(Integer, server_default=text("1100"))
    Health = Column(Integer, server_default=text("4"))
    MaxHealth = Column(Float, server_default=text("4"))
    Armor = Column(Integer, server_default=text("0"))
    MaxArmor = Column(Float, server_default=text("0"))
    Imagination = Column(Integer, server_default=text("0"))
    MaxImagination = Column(Float, server_default=text("0"))
    InventorySpace = Column(Integer, server_default=text("20"))
    UScore = Column(Integer, server_default=text("0"))
    GMLevel = Column(Integer, server_default=text("0"))
    Reputation = Column(Integer, server_default=text("0"))
    Level = Column(Integer, server_default=text("1"))
    X = Column(Float)
    Y = Column(Float)
    Z = Column(Float)


class Inventory(Base):
    __tablename__ = 'Inventory'

    CharID = Column(Integer)
    ItemLOT = Column(Integer)
    IsEquipped = Column(Boolean)
    IsLinked = Column(Boolean)
    Quantity = Column(Integer)
    Slot = Column(Integer)
    ItemID = Column(Integer, primary_key=True, unique=True)
    Type = Column(Integer, server_default=text("0"))


t_Stats = Table(
    'Stats', metadata,
    Column('CharID', Integer),
    Column('CurrencyCollected', Integer, server_default=text("0")),
    Column('BricksCollected', Integer, server_default=text("0")),
    Column('SmashablesSmashed', Integer, server_default=text("0")),
    Column('QuickBuildsCompleted', Integer, server_default=text("0")),
    Column('EnemiesSmashed', Integer, server_default=text("0")),
    Column('RocketsUsed', Integer, server_default=text("0")),
    Column('MissionsCompleted', Integer, server_default=text("0")),
    Column('PetsTamed', Integer, server_default=text("0")),
    Column('ImaginationPowerUpsCollected', Integer, server_default=text("0")),
    Column('LifePowerUpsCollected', Integer, server_default=text("0")),
    Column('ArmorPowerUpsCollected', Integer, server_default=text("0")),
    Column('DistanceTravelled', Integer, server_default=text("0")),
    Column('TimesSmashed', Integer, server_default=text("0")),
    Column('DamageTaken', Integer, server_default=text("0")),
    Column('DamageHealed', Integer, server_default=text("0")),
    Column('ArmorRepaired', Integer, server_default=text("0")),
    Column('ImaginationRestored', Integer, server_default=text("0")),
    Column('ImaginationUsed', Integer, server_default=text("0")),
    Column('DistanceDriven', Integer, server_default=text("0")),
    Column('RaceCarAirborneTime', Integer, server_default=text("0")),
    Column('RacingImaginationPowerUpsCollected', Integer, server_default=text("0")),
    Column('RacingImaginationCratesSmashed', Integer, server_default=text("0")),
    Column('RaceCarBoostsActivated', Integer, server_default=text("0")),
    Column('CarWrecks', Integer, server_default=text("0")),
    Column('RacingSmashablesSmashed', Integer, server_default=text("0")),
    Column('RacesFinished', Integer, server_default=text("0")),
    Column('FirstPlaceRaceWins', Integer, server_default=text("0"))
)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)
