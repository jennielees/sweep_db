from peewee import *
import csv
from datetime import datetime

from sweep import db, Street, SweepTime

# Only run this once (first time)
db.create_tables([Street, SweepTime])

def string_to_time(t):
    # Turns a time of format 'HH:MM' into a native
    # Python time object.
    # http://www.codecademy.com/courses/python-beginner-en-zFPOx/0/1
    # http://effbot.org/librarybook/datetime.htm
    # https://docs.python.org/2/library/datetime.html#time-objects
    d = datetime.strptime(t, '%H:%M')
    return d.time()

def string_to_boolean(s):
    if s == 'True':
        return True
    return False

def create_or_get_street(street_name):
    # Longer alternative to using get_or_create, which peewee
    # advises against.
    # To be even safer we could enforce uniqueness in the database.
    try:
        street = Street.get(Street.name == street_name)
    except:
        street = Street.create(name=street_name)
        street.save()
        print "Created street {}".format(street.name)
    return street

def csv_to_objects(filename):

    with open(filename) as f:
        reader = csv.DictReader(f)

        for row in reader:
            if len(row) != 22:
                print "Error in row data."
                continue # ignore the rest and go to the next item

            d = {}
            street_name = row['CORRIDOR']
            side = row['CNNRIGHTLE']
            if side == 'R':
                d['is_odd'] = False
                d['start'] = row['RT_FADD']
                d['end'] = row['RT_TOADD']
            else:
                d['is_odd'] = True
                d['start'] = row['LF_FADD']
                d['end'] = row['LF_TOADD']
            d['day'] = row['WEEKDAY']
            d['from_hour'] = string_to_time(row['FROMHOUR'])
            d['to_hour']   = string_to_time(row['TOHOUR'])
            d['holidays'] = string_to_boolean(row['HOLIDAYS'])
            d['week1'] = string_to_boolean(row['WEEK1OFMON'])
            d['week2'] = string_to_boolean(row['WEEK2OFMON'])
            d['week3'] = string_to_boolean(row['WEEK3OFMON'])
            d['week4'] = string_to_boolean(row['WEEK4OFMON'])
            d['week5'] = string_to_boolean(row['WEEK5OFMON'])

            # Create the models.
            # First, we might already have created the street,
            # so let's get it if it already exists
            d['street'] = create_or_get_street(street_name)

            # Now, we want to save the new time row.
            sweep_time = SweepTime(**d)
            # this **d syntax is a super cheat way to avoid typing out
            # SweepTime(day=day, is_odd=is_odd...)
            # we put those all in a dictionary, then the ** operator
            # flattens the dictionary out into a list of key=value pairs
            # which is exactly what our SweepTime() constructor wants!
            # http://stackoverflow.com/questions/5710391/converting-python-dict-to-kwargs
            # http://hangar.runway7.net/python/packing-unpacking-arguments
            # http://markmiyashita.com/blog/python-args-and-kwargs/

            sweep_time.save()
            # Note that calling a save() to the database for every
            # row isn't a very efficient way of doing things!


if __name__=="__main__":
    csv_to_objects('sweep.csv')