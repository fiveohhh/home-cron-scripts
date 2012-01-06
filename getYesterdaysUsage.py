#!/usr/bin/python

# Be careful running multiple times a day if you are running near midnight.
# if you are the clock and thermostat are not in sync we could get data that is not from the day we are
# expecting

from TStat import *
import sqlite3
from datetime import datetime, timedelta
import time
import os.path

# get last succesful run time
# we will touch this file if we succesfully run
# if file has not yet been touched in the current day,
# we will get the previous days usage

FILE = 'getYesterdaysUsage'
getUsage = False
if not os.path.exists(FILE):
    open(FILE,'a').close()
    getUsage=True # getUsage if we have to create the file

# get last time FILE was modified
lastSuccess =  time.ctime(os.path.getmtime(FILE))
dateLastSuccess = datetime.strptime(lastSuccess,'%a %b %d %H:%M:%S %Y')

#If file was modified on a day that is not today, update usage stats
if dateLastSuccess.day != datetime.now().day:
    getUsage = True

if getUsage == True:
    t = TStat('10.12.34.139')
    heatUsage = t.getHeatUsageYesterday()
    coolUsage = t.getCoolUsageYesterday()

    heatMinutes = heatUsage['hour'] * 60 + heatUsage['minute']
    coolMinutes = coolUsage['hour'] * 60 + coolUsage['minute']
    currentTime = int(round(time.time()))

    conn = sqlite3.connect('/home/andy/djangoProjects/leeHouseSite/sqlite/db.sql3')
    c = conn.cursor()
    c.execute("insert into restInterface_hvac_runtime values (NULL," + str(currentTime) + "," + str(heatMinutes) +"," + str(coolMinutes) + ")")
    conn.commit()

