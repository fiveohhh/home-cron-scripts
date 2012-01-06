#!/usr/bin/python

# When this is ran, if the last door entry for the garage(doorNumber = 0)
# is open, Let's get the time that it was opened and compare it to the current
# time, if it is greater than MINUTES_TILL_WARNING_SENT, send a warning email

MINUTES_TILL_WARNING_SENT = 60

from datetime import datetime
from sendEmail import SendEmail
import sqlite3


dirOfThisFile = os.path.dirname(__file__)

# get settings
settingsRaw = open(dirOfThisFile + '/../houseSettings', 'r').read().strip()
settings = dict(item.split(':') for item in settingsRaw.split('\n'))


conn = sqlite3.connect('/home/andy/djangoProjects/leeHouseSite/sqlite/db.sql3')
c = conn.cursor()
c.execute('select * from restInterface_door_entry where id = (select max(id) from restInterface_door_entry) and doorNumber = 0')

# will only be one entry, the last one entered in the table. get it
lastGarage = c.fetchone()
doorStatus = lastGarage[2]

# If door is open
if doorStatus == 1:
    timeDoorHasBeenOpen = datetime.now() - datetime.fromtimestamp(lastGarage[3])
    if timeDoorHasBeenOpen.minutes > MINUTES_TILL_WARNING_SENT:
        # if warning time has passed
        message = "Subject:House Warning: Garage door is OPEN.\n\nHas been open since: "
        message += str(datetime.fromtimestamp(lastGarage[3]))
        SendEmail(settings['WARNING_EMAIL1'], message)
        SendEmail(settings['WARNING_EMAIL2'], message)
