#!/usr/bin/python

# When this is ran, if the last door entry for the garage(doorNumber = 0)
# is open, Let's get the time that it was opened and compare it to the current
# time, if it is greater than MINUTES_TILL_WARNING_SENT, send a warning email

MINUTES_TILL_WARNING_SENT = 30

from datetime import datetime
from sendEmail import SendEmail
import sqlite3
import os
from ConfigParser import SafeConfigParser

GARAGE_DOOR_SENSORS = [0,1]

dirOfThisFile = os.path.dirname(__file__)

# get settings
parser = SafeConfigParser()
print dirOfThisFile
parser.read('/home/andy/houseSettings')
warning_email_1 = parser.get('core settings','WARNING_EMAIL1')
warning_email_2 = parser.get('core settings','WARNING_EMAIL2')

conn = sqlite3.connect('/home/andy/djangoProjects/leeHouseSite/sqlite/db.sql3')
c = conn.cursor()
for row in c.execute('select t1.* FROM restInterface_door_entry AS t1 LEFT OUTER JOIN restInterface_door_entry AS t2 ON (t1.doorNumber = t2.doorNumber AND t1.id < t2.id) where t2.doorNumber IS NULL;'):
    if row[1] in GARAGE_DOOR_SENSORS:
        # This door entry is a garage door
        lastGarage = row
        doorStatus = row[2]
        if doorStatus == 1:
            timeDoorHasBeenOpen = datetime.now() - datetime.fromtimestamp(lastGarage[3])
            if timeDoorHasBeenOpen.seconds/60 > MINUTES_TILL_WARNING_SENT:
                # if warning time has passed
                message = "Subject:House Warning: Garage door is OPEN.\n\nHas been open since: "
                message += str(datetime.fromtimestamp(lastGarage[3]))
                SendEmail(warning_email_1, message)
                SendEmail(warning_email_2, message)




