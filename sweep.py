from peewee import *

db = SqliteDatabase('peewee.db')

class Street(Model):
    # Have street name in its own model, since it is repeated
    # a lot and represents its own entity
    name = CharField()

class SweepTime(Model):
    # Represent the time of the sweeping
    day = CharField()
    from_hour = TimeField()
    to_hour = TimeField()
    holidays = BooleanField()
    week1 = BooleanField()
    week2 = BooleanField()
    week3 = BooleanField()
    week4 = BooleanField()
    week5 = BooleanField()
    # Represent the starting block #, the end block #, and
    # whether it is the odd or even side of the street
    start  = IntegerField()
    end    = IntegerField()
    is_odd = BooleanField()

    # Link to the street. Since a street has many times, we
    # put the reference on the SweepTime side.
    street = ForeignKeyField(Street, related_name="times")
